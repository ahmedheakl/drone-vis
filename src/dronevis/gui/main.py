from tkinter import Tk, HORIZONTAL, LEFT, StringVar
from tkinter.ttk import Label, Frame, Style, Progressbar, OptionMenu
from dronevis.gui.configs import *
from dronevis.gui.image_bw_button import ImageBWButton
from dronevis.gui.main_button import MainButton
from dronevis.drone_connect.drone import Drone
from dronevis.drone_connect.demo_drone import DemoDrone
from dronevis.detection_torch import YOLOv5
import matplotlib.pyplot as plt
from dronevis.gui.circular_progressbar import CircularProgressbar
from dronevis.gui.navdata_frame import DataFrame
from typing import Union
from dronevis.abstract import NOOPModel
from dronevis.detection_torch import YOLOv5, SSD
from dronevis.face_detection import FaceDetectModel


class DroneVisGui:
    def __init__(
        self,
        drone: Union[Drone, DemoDrone, None] = None,
        mode: str = "real",
    ) -> None:
        """Contruct a GUI window

        Args:
            drone (Union[Drone, DemoDrone, None], optional): drone instance for connection.
                If the you don't provide an instance a demo will be run. Defaults to None.
        """
        if mode not in ["real", "demo"]:
            raise ValueError("Please enter a valid mode, either `real` or `demo`.")
        self.mode = mode
        window = Tk()
        self.drone = drone if drone else DemoDrone()
        self.window = window
        self.is_stream = False

        ################# Configurations #######################
        window.protocol("WM_DELETE_WINDOW", self.on_close_window)
        window.geometry("1000x580")
        s = Style()
        s.theme_use("clam")
        s.configure(".", font=MAIN_FONT, background=MAIN_COLOR, foreground=WHITE_COLOR)
        s.configure("MainFrame.TFrame", relief="solid", borderwidth=1)
        s.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=WHITE_COLOR,
            background=GREEN_COLOR,
        )
        window.title("Drone Vision")
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, minsize=600, weight=1)
        window.columnconfigure(1, minsize=330, weight=1)

        self.ax = None
        self.init_demo_data()
        self.init_frames()
        
    def init_demo_data(self):
        self.data = [0]
        self.index = [0]
        self.step_index = 0.2
        self.mid_point = int((20.0 / self.step_index) // 2)

    def axis_config(self, ax) -> None:
        """Set the axis paramets for height graph

        Args:
            ax (plt.ax): matplotlib axis
        """
        ax.legend(["height"])
        ax.set_xlabel("Time")
        ax.set_ylabel("Height")
        ax.yaxis.label.set_color(WHITE_COLOR)
        ax.xaxis.label.set_color(WHITE_COLOR)
        ax.title.set_color(WHITE_COLOR)
        ax.spines["bottom"].set_color(WHITE_COLOR)
        ax.spines["top"].set_color(WHITE_COLOR)
        ax.spines["right"].set_color(WHITE_COLOR)
        ax.spines["left"].set_color(WHITE_COLOR)
        ax.tick_params(axis="x", colors=WHITE_COLOR)
        ax.tick_params(axis="y", colors=WHITE_COLOR)
        ax.set_facecolor(MAIN_COLOR)
        ax.set_ylim([0, 50])
        ax.set_xlim([0, 20])

    def on_plot(self) -> None:
        """Handles heights points and graph them"""
        if self.ax is None:
            figure3 = plt.figure(figsize=(5, 4), dpi=90)  # type
            figure3.set_facecolor(MAIN_COLOR)
            self.ax = figure3.add_subplot(111)
            self.ax.plot(self.index, self.data, color="g", linewidth=2)
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            self.scatter3 = FigureCanvasTkAgg(figure3, self.frm_nav_h)
            self.scatter3.get_tk_widget().grid(
                row=0, column=0, sticky="nsew", pady=5, padx=5
            )
            self.axis_config(self.ax)
        else:
            if len(self.index) > self.mid_point * 2:
                
                # shifting data to left
                first_point = self.index[self.mid_point]
                self.index = self.index[self.mid_point :]
                self.index = [i - first_point for i in self.index]
                self.data = self.data[self.mid_point :]
                self.cnt = len(self.index)
                self.ax.clear()
                self.scatter3.draw()

            self.ax.plot(self.index, self.data, color="g", linewidth=2)
            self.axis_config(self.ax)
            self.scatter3.draw()

    def init_frames(self):
        """Initialize main frames for the GUI"""
        frm_left = Frame(master=self.window)
        frm_right = Frame(master=self.window)

        # Left Configs
        frm_left.rowconfigure(0, minsize=480, weight=1)
        frm_left.rowconfigure(1, minsize=100, weight=1)
        frm_left.columnconfigure(0, minsize=600, weight=1)

        # Right Configs
        frm_right.columnconfigure(0, minsize=400, weight=1)
        frm_right.rowconfigure(0, minsize=280, weight=1)
        frm_right.rowconfigure(1, minsize=180, weight=1)
        frm_right.rowconfigure(2, minsize=120, weight=1)

        frm_info = Frame(master=frm_left)
        frm_info.rowconfigure(0, weight=2)
        frm_info.rowconfigure(1, weight=3)
        # frm_info.rowconfigure(2, weight=2)
        frm_info.columnconfigure(0, weight=1)

        ######################## Battary Data ###################################
        frm_battary = Frame(frm_info, style="MainFrame.TFrame")
        lbl_battary = Label(frm_battary, text="Battery Percentage", font=HEADER_FONT)
        frm_progress = Frame(frm_battary)
        self.pb_battery = Progressbar(
            frm_progress,
            mode="determinate",
            length=300,
            maximum=100,
            orient=HORIZONTAL,
            value=0,
            style="Custom.Horizontal.TProgressbar",
        )

        self.lbl_battery_percentage = Label(frm_progress, text="Connect to drone")

        frm_battary.rowconfigure(0, weight=1)
        frm_battary.rowconfigure(2, weight=1)
        frm_battary.columnconfigure(0, weight=1)

        ####################### Graphs and Navdata ##############################
        frm_nav_h = Frame(frm_info, style="MainFrame.TFrame")
        frm_nav_h.columnconfigure(0, weight=4)
        frm_nav_h.columnconfigure(0, weight=2)
        frm_nav_h.rowconfigure(0, weight=1)
        self.frm_nav_h = frm_nav_h

        self.on_plot()

        frm_navdata = Frame(frm_nav_h)
        frm_navdata.rowconfigure(0, weight=1)
        frm_navdata.rowconfigure(1, weight=1)
        frm_navdata.rowconfigure(2, weight=1)

        self.frm_nav_vx = DataFrame(frm_navdata, title="vx")
        self.frm_nav_vx.grid(row=0, column=0, sticky="ew")

        self.frm_nav_vy = DataFrame(frm_navdata, title="vy")
        self.frm_nav_vy.grid(row=1, column=0, sticky="ew")

        self.frm_nav_vz = DataFrame(frm_navdata, title="vz")
        self.frm_nav_vz.grid(row=2, column=0, sticky="ew")

        ######################## Basic Control ##################################
        frm_basic_control = Frame(master=frm_right, style="MainFrame.TFrame")
        lbl_basic_control = Label(
            frm_basic_control, text="Basic Control", font=HEADER_FONT
        )

        btn_forward = ImageBWButton(
            frm_basic_control,
            title="FORWARD",
            message="Move the drone forward",
            img="forward.png",
            size=VERTICAL_ARROW_SIZE,
            command=self.drone.forward,
        )
        btn_backward = ImageBWButton(
            frm_basic_control,
            title="BACKWARD",
            message="Move the drone Backword",
            img="backward.png",
            size=VERTICAL_ARROW_SIZE,
            command=self.drone.backward,
        )
        btn_right = ImageBWButton(
            frm_basic_control,
            title="RIGHT",
            message="Move the drone to the right",
            img="right.png",
            size=HORIZONTAL_ARROW_SIZE,
            command=self.drone.right,
        )
        btn_left = ImageBWButton(
            frm_basic_control,
            title="LFET",
            message="Move the drone to the left",
            img="left.png",
            size=HORIZONTAL_ARROW_SIZE,
            command=self.drone.left,
        )
        btn_rotate_l = ImageBWButton(
            frm_basic_control,
            title="ROT L",
            message="Rotate the drone to the left",
            img="rotate_ccw.png",
            size=(35, 30),
            command=self.drone.rotate_left,
        )
        btn_rotate_r = ImageBWButton(
            frm_basic_control,
            title="ROT R",
            message="Rotate the drone to the right",
            img="rotate_cw.png",
            size=(35, 30),
            command=self.drone.rotate_right,
        )
        btn_up = ImageBWButton(
            frm_basic_control,
            title="UPWARD",
            message="Move the drone up",
            img="up.png",
            size=VERTICAL_ARROW_SIZE,
            command=self.drone.up,
        )
        btn_down = ImageBWButton(
            frm_basic_control,
            title="DOWN",
            message="Move the drone down",
            img="down.png",
            size=VERTICAL_ARROW_SIZE,
            command=self.drone.down,
        )

        self.btn_connect = MainButton(
            frm_basic_control,
            message="Start drone connection",
            text="START",
        )

        self.btn_connect.bind("<Button-1>", self.on_drone_connect)

        for i in range(4):
            frm_basic_control.rowconfigure(i, weight=1)
            frm_basic_control.columnconfigure(i % 3, minsize=70, weight=1)

        ######################## Special Control #################################
        frm_special_control = Frame(master=frm_right, style="MainFrame.TFrame")
        lbl_special_control = Label(
            frm_special_control,
            text="Special Control",
            font=HEADER_FONT,
        )
        btn_take_off = MainButton(
            frm_special_control,
            message="The drone takes off the ground",
            text="Take off",
            command=self.drone.takeoff,
        )
        btn_land = MainButton(
            frm_special_control,
            message="The drone lands smoothly",
            text="Land",
            command=self.drone.land,
        )
        btn_hover = MainButton(
            frm_special_control,
            message="The drone hovers in its position",
            text="Hover",
            command=self.drone.hover,
        )
        btn_flip = MainButton(
            frm_special_control,
            message="The drone flip 360 degrees",
            text="Flip",
        )

        for i in range(3):
            frm_special_control.rowconfigure(i, weight=1)
            frm_special_control.columnconfigure(i % 2, minsize=140, weight=1)

        ######################## Reset Control #################################
        frm_reset_control = Frame(frm_right, style="MainFrame.TFrame")
        lbl_reset_control = Label(
            frm_reset_control, text="Reset Control", font=HEADER_FONT
        )
        btn_reset = MainButton(
            frm_reset_control,
            text="Reset",
            message="Reset drone states. Use it when a red led turns on",
            command=self.drone.reset,
        )
        btn_calib = MainButton(
            frm_reset_control,
            text="Caliberate",
            message="Caliberate drone sensors",
            command=self.drone.calibrate,
        )
        btn_emerg = MainButton(
            frm_reset_control,
            text="Emergency",
            message="Set drone in emergency state",
            command=self.drone.emergency,
        )

        for i in range(3):
            frm_reset_control.rowconfigure(i % 2, weight=1)
            frm_reset_control.columnconfigure(i, minsize=70, weight=1)

        ######################## Vision Control ##################################
        frm_vision_control = Frame(master=frm_left, style="MainFrame.TFrame")
        lbl_vision_control = Label(
            frm_vision_control, text="Vision Control", font=HEADER_FONT
        )
        btn_record_video = MainButton(
            master=frm_vision_control,
            text="Record",
            message="Record a video which will be saved on drone controller memory",
        )
        self.clicked = StringVar()
        self.clicked.set("none")
        self.models = {
            "none": NOOPModel,
            "yolov5": YOLOv5,
            "ssd": SSD,
            "face": FaceDetectModel
        }
        btn_detection = OptionMenu(
            frm_vision_control,
            self.clicked,
            *self.models.keys()
        )

        self.btn_video_stream = MainButton(
            frm_vision_control,
            text="Stream",
            message="Initiate video stream from drone",
            command=self.on_stream,
        )

        for i in range(3):
            frm_vision_control.rowconfigure(i % 2, weight=1)
            frm_vision_control.columnconfigure(i, minsize=200, weight=1)

        ######################## Placement ##################################
        # basic control
        lbl_basic_control.grid(row=0, columnspan=4, pady=5, padx=5)
        btn_forward.grid(row=1, column=1, sticky="ew", padx=2)
        btn_backward.grid(row=3, column=1, sticky="ew", padx=2)
        btn_right.grid(row=2, column=2, sticky="ew", padx=5)
        btn_left.grid(row=2, column=0, sticky="ew", padx=2)
        btn_up.grid(row=3, column=2, sticky="ew", padx=5)
        btn_down.grid(row=3, column=0, sticky="ew", padx=5)
        btn_rotate_l.grid(row=1, column=0, sticky="ew", padx=5)
        btn_rotate_r.grid(row=1, column=2, sticky="ew", padx=2)
        self.btn_connect.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # special control
        lbl_special_control.grid(row=0, columnspan=2, pady=5, padx=5)
        btn_take_off.grid(row=1, column=0, sticky="ew", padx=5)
        btn_land.grid(row=1, column=1, sticky="ew", padx=5)
        btn_hover.grid(row=2, column=0, sticky="ew", padx=5)
        btn_flip.grid(row=2, column=1, sticky="ew", padx=5)

        # reset control
        lbl_reset_control.grid(row=0, columnspan=3, padx=5)
        btn_reset.grid(row=1, column=0, sticky="ew", padx=5, ipady=2)
        btn_calib.grid(row=1, column=1, sticky="ew", padx=5, ipady=2)
        btn_emerg.grid(row=1, column=2, sticky="ew", padx=5, ipady=2)

        # battary info
        lbl_battary.grid(row=0, column=0)
        self.pb_battery.pack(side=LEFT)
        self.lbl_battery_percentage.pack(side=LEFT, padx=5)
        frm_progress.grid(row=2, column=0)

        # height graph
        frm_nav_h.grid(row=1, column=0, sticky="nsew")
        frm_navdata.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

        # vision control
        lbl_vision_control.grid(row=0, column=1, pady=10)
        btn_record_video.grid(row=1, column=0, sticky="ew", padx=10, pady=10, ipady=2)
        btn_detection.grid(row=1, column=1, sticky="ew", padx=10, pady=10, ipady=2)
        self.btn_video_stream.grid(row=1, column=2, sticky="ew", padx=10, pady=10, ipady=2)

        # Left Frame
        frm_vision_control.grid(row=1, column=0, sticky="nsew")
        frm_info.grid(row=0, column=0, sticky="nsew")
        frm_battary.grid(row=0, column=0, sticky="nsew")

        # Right Frame
        frm_basic_control.grid(row=0, column=0, sticky="nsew")
        frm_special_control.grid(row=1, column=0, sticky="nsew")
        frm_reset_control.grid(row=2, column=0, sticky="nsew")

        frm_left.grid(row=0, column=0, sticky="nsew")
        frm_right.grid(row=0, column=1, sticky="nsew")

    def on_close_window(self):
        """Event handler for closing the GUI window

        It stop the drone connection and destroyes and GUI window
        """
        self.drone.stop()
        self.window.destroy()

    def on_drone_connect(self, e):
        """Event handler for drone connection

        Args:
            e (tkiner.Event): event for pressing on start button
        """
        self.drone.connect() # connect drone
        self.drone.set_config(activate_gps=True, activate_navdata=True)
        
        
        # change connect button color
        self.btn_connect["text"] = "Connected"
        self.btn_connect["background"] = GREEN_COLOR
        self.btn_connect["foreground"] = WHITE_COLOR
        self.btn_connect["activebackground"] = RED_COLOR
        self.btn_connect["activeforeground"] = WHITE_COLOR
        
        # set navdata handler as callback
        self.drone.set_callback(self.on_navdata)
        
    def on_navdata(self, navdata):
        """Callback handler to retrieve navdata from drone instance

        Args:
            navdata (dict): navigation data dictionary
        """
        if not self.drone.is_connected:
            return

        # battery handling
        battery_percentage = int(navdata["navdata_demo"]["battery_percentage"])
        self.pb_battery["value"] = battery_percentage
        self.lbl_battery_percentage["text"] = f"{battery_percentage}%"
        
        # velocity handling
        to_angle = lambda x, mx: (x/mx) * 360.0
        vx = int(navdata["navdata_demo"]["vx"])
        vx_text = f"{abs(vx)} km\\h"
        self.frm_nav_vx.cpb.change(to_angle(abs(vx), 17.0), vx_text)
        
        vy = int(navdata["navdata_demo"]["vy"])
        vy_text = f"{abs(vy)} km\\h"
        self.frm_nav_vy.cpb.change(to_angle(abs(vy), 17.0), vy_text)
        
        vz = int(navdata["navdata_demo"]["vz"])
        vz_text = f"{abs(vz)} km\\h"
        self.frm_nav_vz.cpb.change(to_angle(abs(vz), 17.0), vz_text)
        
        # elevation handling
        h = int(navdata["navdata_demo"]["altitude"])
        self.data.append(h)
        last_index = self.index[-1]
        self.index.append(last_index + self.step_index) # type: ignore
        self.on_plot()
        
    def on_stream(self):
        """Event handler for pressing on stream button"""
        if self.drone.video_thread is None:
            print(self.clicked.get())
            model = self.models[self.clicked.get()]()
            model.load_model()
            self.drone.connect_video(self.close_stream_callback, model)
            self.btn_video_stream["text"] = "streaming"
            
        else:
            self.drone.disconnect_video()
            
    def close_stream_callback(self):
        self.btn_video_stream["text"] = "Stream"


def main():
    drone = Drone()
    gui = DroneVisGui(drone=drone)
    gui.window.mainloop()
