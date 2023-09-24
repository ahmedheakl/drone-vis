"""GUI implmentation"""
from typing import Optional, List

from tkinter import Tk, StringVar, HORIZONTAL, LEFT
from tkinter.ttk import Style, Frame, Label, Progressbar, OptionMenu
import logging
from dataclasses import dataclass, field
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
import numpy as np
from PIL import Image, ImageTk

from dronevis.models import models_list
from dronevis.drone_connect import DemoDrone
from dronevis.abstract.base_drone import BaseDrone
from dronevis.utils.general import axis_config
from dronevis.config import gui as cfg
from dronevis.ui.gui_components import (
    ImageBWButton,
    MainButton,
    DataFrame,
    ToggleButton,
)
from dronevis.ui.gesture_recognition_thread import GestureThread
from dronevis.models import CrowdCounter

_LOG = logging.getLogger(__name__)
CROWD_TOCKS = 5


@dataclass
class GUIOpt:
    """GUI attributes"""

    axis: Optional[plt.Axes] = None
    navdata: Optional[dict] = None
    plot_job: Optional[str] = None
    data: List[int] = field(default_factory=lambda: [0])
    index: List[float] = field(default_factory=lambda: [0.0])
    scatter: Optional[FigureCanvasTkAgg] = None


@dataclass
class GUIFrames:
    """GUI Frames"""

    pb_battery: Progressbar
    lbl_battery_percentage: Label
    frm_nav_vx: DataFrame
    frm_nav_vy: DataFrame
    frm_nav_vz: DataFrame
    btn_connect: MainButton
    btn_video_stream: MainButton
    lbl_count: Label
    btn_control_gesture: ToggleButton


class DroneVisGui:
    """Implementation for the library GUI using Tkinter"""

    mid_point = int((cfg.GUI_X_LIMIT / cfg.INDEX_STEP) // 2)

    def __init__(
        self,
        drone: Optional[BaseDrone] = None,
    ) -> None:
        """Contruct a GUI window

        Args:
            drone (Union[Drone, DemoDrone, None], optional): drone instance for connection.
                If the you don't provide an instance a demo will be run. Defaults to None.
        """
        self.window = Tk()
        self.drone = drone if drone else DemoDrone()

        ################# Configurations #######################
        _LOG.debug("Initializing root window ...")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close_window)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        window_style = Style()
        window_style.theme_use("clam")
        window_style.configure(
            ".",
            font=cfg.MAIN_FONT,
            background=cfg.MAIN_COLOR,
            foreground=cfg.FONT_COLOR,
        )
        window_style.configure("MainFrame.TFrame", relief="solid", borderwidth=1)
        window_style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=cfg.WHITE_COLOR,
            background=cfg.GREEN_COLOR,
        )
        self.window.title("Drone Vision")
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=2)
        self.window.columnconfigure(1, weight=1)

        # attributes initializations
        self.opt = GUIOpt()
        self.init_frames()
        self.gesture_thread: Optional[GestureThread] = None
        self.is_crowdcount = False
        self.crowd_model = CrowdCounter()
        self.crowd_tick = 0
        _LOG.debug("Main frames initialized")

    def handle_navdata(self) -> None:
        """Handle incomming navdata and convert them to suitable format"""
        if self.opt.navdata is None:
            return

        navdata = self.opt.navdata

        # Battery comes in percentage format
        battery_percentage = int(navdata["navdata_demo"]["battery_percentage"])
        self.frms.pb_battery["value"] = battery_percentage
        self.lbl_battery_percentage["text"] = f"{battery_percentage}%"

        # Velocity comes in mm/s format
        vel_x = navdata["navdata_demo"]["vx"] * cfg.MILLI_TO_METER_FACTOR
        vx_text = f"{abs(vel_x):0.2f} m\\s"
        self.frms.frm_nav_vx.cpb.change(to_angle(abs(vel_x), cfg.MAX_VELOCITY), vx_text)

        vel_y = navdata["navdata_demo"]["vy"] * cfg.MILLI_TO_METER_FACTOR
        vy_text = f"{abs(vel_y):0.2f} m\\s"
        self.frms.frm_nav_vy.cpb.change(to_angle(abs(vel_y), cfg.MAX_VELOCITY), vy_text)

        vel_z = navdata["navdata_demo"]["vz"] * cfg.MILLI_TO_METER_FACTOR
        vz_text = f"{abs(vel_z):0.2f} m\\s"
        self.frms.frm_nav_vz.cpb.change(to_angle(abs(vel_z), cfg.MAX_VELOCITY), vz_text)

        # Elevation comes in mm format
        elevation = int(navdata["navdata_demo"]["altitude"] * cfg.MILLI_TO_METER_FACTOR)
        self.opt.data.append(elevation)
        last_index = self.opt.index[-1]
        self.opt.index.append(last_index + cfg.INDEX_STEP)

    def on_plot(self) -> None:
        """Handles heights points and graph them"""

        # Convert incoming navdata to suitable format
        self.handle_navdata()

        # Initialize axis if not exist
        if self.opt.axis is None or self.opt.scatter is None:
            # Initialize a figure instance
            figure3 = plt.figure(figsize=(5, 4), dpi=90)

            # Set background color to MAIN COLOR
            figure3.set_facecolor(cfg.MAIN_COLOR)

            # Create a subplot instance stored in self.axis
            self.opt.axis = figure3.add_subplot(111)

            # Plot data on created axis
            self.opt.axis.plot(self.opt.index, self.opt.data, color="g", linewidth=2)

            # Create a tkinter widget with axis object
            self.opt.scatter = FigureCanvasTkAgg(figure3, self.frm_nav_h)

            # Place the plotting-tkiner widget
            self.opt.scatter.get_tk_widget().grid(
                row=0,
                column=0,
                sticky="nsew",
                pady=5,
                padx=5,
            )

            # Set configurations for the axis
            axis_config(self.opt.axis)

        else:
            # if number of points exceeded the width of the graph
            if len(self.opt.index) > self.mid_point * 2:
                # shifting data to left
                first_point = self.opt.index[self.mid_point]
                self.opt.index = self.opt.index[self.mid_point :]
                self.opt.index = [i - first_point for i in self.opt.index]
                self.opt.data = self.opt.data[self.mid_point :]
                self.opt.axis.clear()
                self.opt.scatter.draw()

            # plot updated data and reset configs
            self.opt.axis.plot(self.opt.index, self.opt.data, color="g", linewidth=2)
            axis_config(self.opt.axis)
            self.opt.scatter.draw()

        # recursive call to the plot function to run each 51 ms
        self.opt.plot_job = self.window.after(ms=51, func=self.on_plot)

    # pylint: disable=too-many-statements,too-many-locals
    def init_frames(self):
        """Initialize main frames for the GUI"""
        frm_left = Frame(master=self.window)
        frm_right = Frame(master=self.window)

        # Left Configs
        frm_left.rowconfigure(0, weight=2)
        frm_left.rowconfigure(1, weight=3)
        frm_left.columnconfigure(0, weight=1)

        # Right Configs
        frm_right.columnconfigure(0, weight=1)
        frm_right.rowconfigure(0, minsize=120, weight=1)
        frm_right.rowconfigure(1, minsize=120, weight=1)
        frm_right.rowconfigure(2, minsize=120, weight=1)
        frm_right.rowconfigure(3, minsize=120, weight=1)
        frm_right.rowconfigure(4, minsize=120, weight=1)
        frm_right.rowconfigure(5, minsize=120, weight=1)
        ######################## Camera Feed ###################################
        frm_camera = Frame(frm_left, style="MainFrame.TFrame")
        frm_camera.rowconfigure(0, weight=1)
        frm_camera.rowconfigure(1, weight=5)
        frm_camera.columnconfigure(0, weight=1)
        frm_camera.columnconfigure(1, weight=1)
        lbl_camera = Label(
            frm_camera,
            text="Camera Feed",
            font=cfg.HEADER_FONT,
            anchor="center",
        )
        self.camera_feed = Label(
            frm_camera,
            text="Camera Feed",
            font=cfg.HEADER_FONT,
            anchor="center",
        )
        lbl_gesture = Label(
            frm_camera,
            text="Gesture Feed",
            font=cfg.HEADER_FONT,
            anchor="center",
        )
        self.gesture_feed = Label(
            frm_camera,
            text="Gesture Feed",
            font=cfg.HEADER_FONT,
            anchor="center",
        )

        black_image = np.array([[[0, 0, 0]] * 400] * 380, dtype=np.uint8)
        img = Image.fromarray(black_image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.gesture_feed.imgtk = imgtk
        self.gesture_feed.configure(image=imgtk)
        ######################## Battary Data ###################################
        frm_battary = Frame(frm_right, style="MainFrame.TFrame")
        lbl_battary = Label(
            frm_battary, text="Battery Percentage", font=cfg.HEADER_FONT
        )
        frm_progress = Frame(frm_battary)
        pb_battery = Progressbar(
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
        ####################### Fine Controls ##################################
        frm_fine_control = Frame(frm_right, style="MainFrame.TFrame")
        frm_fine_control.rowconfigure(0, weight=1)
        frm_fine_control.rowconfigure(1, weight=1)
        frm_fine_control.columnconfigure(0, weight=1)
        frm_fine_control.columnconfigure(1, weight=1)
        lbl_control_gesture = Label(frm_fine_control, text="Gesture")
        btn_control_gesture = ToggleButton(
            frm_fine_control,
            self.on_gesture,
            self.off_gesture,
        )
        lbl_control_gesture.grid(row=0, column=0)
        btn_control_gesture.grid(row=1, column=0)
        lbl_control_crowd = Label(frm_fine_control, text="Crowd")
        btn_control_gesture = ToggleButton(
            frm_fine_control, self.on_crowd, self.on_crowd
        )
        lbl_control_crowd.grid(row=0, column=1)
        btn_control_gesture.grid(row=1, column=1)

        ####################### Graphs and Navdata ##############################
        frm_nav_h = Frame(frm_left, style="MainFrame.TFrame")
        frm_nav_h.columnconfigure(0, weight=4)
        frm_nav_h.columnconfigure(0, weight=2)
        frm_nav_h.rowconfigure(0, weight=1)
        self.frm_nav_h = frm_nav_h

        self.on_plot()

        frm_navdata = Frame(frm_nav_h)
        frm_navdata.rowconfigure(0, weight=2)
        frm_navdata.rowconfigure(1, weight=2)
        frm_navdata.rowconfigure(2, weight=2)
        frm_navdata.rowconfigure(3, weight=3)

        frm_nav_vx = DataFrame(frm_navdata, title="vx")
        frm_nav_vx.grid(row=0, column=0, sticky="ew")

        frm_nav_vy = DataFrame(frm_navdata, title="vy")
        frm_nav_vy.grid(row=1, column=0, sticky="ew")

        frm_nav_vz = DataFrame(frm_navdata, title="vz")
        frm_nav_vz.grid(row=2, column=0, sticky="ew")

        frm_crowd = Frame(frm_navdata)
        frm_crowd.rowconfigure(0, weight=1)
        frm_crowd.rowconfigure(1, weight=1)
        frm_crowd.columnconfigure(0, weight=1)

        lbl_crowd = Label(frm_crowd, text="Crowd Count")
        lbl_crowd.grid(row=0, column=0, sticky="ew")
        lbl_count = Label(frm_crowd, text="0", anchor="center")
        lbl_count.grid(row=1, column=0, sticky="ew")
        frm_crowd.grid(row=3, column=0, sticky="ew")

        ######################## Basic Control ##################################
        frm_basic_control = Frame(master=frm_right, style="MainFrame.TFrame")
        lbl_basic_control = Label(
            frm_basic_control, text="Basic Control", font=cfg.HEADER_FONT
        )

        btn_forward = ImageBWButton(
            frm_basic_control,
            title="FORWARD",
            message="Move the drone forward",
            img="forward.png",
            size=cfg.VERTICAL_ARROW_SIZE,
            command=self.drone.forward,
        )
        btn_backward = ImageBWButton(
            frm_basic_control,
            title="BACKWARD",
            message="Move the drone Backword",
            img="backward.png",
            size=cfg.VERTICAL_ARROW_SIZE,
            command=self.drone.backward,
        )
        btn_right = ImageBWButton(
            frm_basic_control,
            title="RIGHT",
            message="Move the drone to the right",
            img="right.png",
            size=cfg.HORIZONTAL_ARROW_SIZE,
            command=self.drone.right,
        )
        btn_left = ImageBWButton(
            frm_basic_control,
            title="LFET",
            message="Move the drone to the left",
            img="left.png",
            size=cfg.HORIZONTAL_ARROW_SIZE,
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
            size=cfg.VERTICAL_ARROW_SIZE,
            command=self.drone.upward,
        )
        btn_down = ImageBWButton(
            frm_basic_control,
            title="DOWN",
            message="Move the drone down",
            img="down.png",
            size=cfg.VERTICAL_ARROW_SIZE,
            command=self.drone.downward,
        )

        btn_connect = MainButton(
            frm_basic_control,
            message="Start drone connection",
            text="START",
        )

        btn_connect.bind("<Button-1>", self.on_drone_connect)

        for i in range(4):
            frm_basic_control.rowconfigure(i, weight=1)
            frm_basic_control.columnconfigure(i % 3, minsize=70, weight=1)

        ######################## Special Control #################################
        frm_special_control = Frame(master=frm_right, style="MainFrame.TFrame")
        lbl_special_control = Label(
            frm_special_control,
            text="Special Control",
            font=cfg.HEADER_FONT,
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
            frm_reset_control, text="Reset Control", font=cfg.HEADER_FONT
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
        frm_vision_control = Frame(frm_right, style="MainFrame.TFrame")
        lbl_vision_control = Label(
            frm_vision_control, text="Vision Control", font=cfg.HEADER_FONT
        )
        btn_record_video = MainButton(
            master=frm_vision_control,
            text="Record",
            message="Record a video which will be saved on drone controller memory",
        )
        self.models_choice = StringVar()
        self.models_choice.set("None")
        style = Style()
        style.configure(
            "TMenubutton",
            foreground=cfg.FONT_COLOR,
            background=cfg.BUTTON_COLOR,
        )
        btn_detection = OptionMenu(
            frm_vision_control,
            self.models_choice,
            *models_list.keys(),
        )

        def on_enter_menu(_):
            style.map(
                "TMenubutton",
                foreground=[("active", cfg.MAIN_COLOR)],
                background=[("active", cfg.WHITE_COLOR)],
            )

        def on_leave_menu(_):
            style.map(
                "TMenubutton",
                foreground=[("active", cfg.FONT_COLOR)],
                background=[("active", cfg.BUTTON_COLOR)],
            )

        btn_detection.bind("<Enter>", on_enter_menu)
        btn_detection.bind("<Leave>", on_leave_menu)

        btn_video_stream = MainButton(
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
        btn_connect.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

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
        pb_battery.pack(side=LEFT)
        self.lbl_battery_percentage.pack(side=LEFT, padx=5)
        frm_progress.grid(row=2, column=0)

        # height graph
        frm_navdata.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

        # vision control
        lbl_vision_control.grid(row=0, column=1, pady=10)
        btn_record_video.grid(row=1, column=0, sticky="ew", padx=10, pady=10, ipady=2)
        btn_detection.grid(row=1, column=1, sticky="ew", padx=10, pady=10, ipady=2)
        btn_video_stream.grid(row=1, column=2, sticky="ew", padx=10, pady=10, ipady=2)

        # camera feed
        lbl_camera.grid(row=0, column=0, sticky="nsew")
        lbl_gesture.grid(row=0, column=1, sticky="nsew")
        self.camera_feed.grid(row=1, column=0, sticky="nsew")
        self.gesture_feed.grid(row=1, column=1, sticky="nsew")

        # Left Frame
        frm_camera.grid(row=0, column=0, sticky="nsew")
        frm_nav_h.grid(row=1, column=0, sticky="nsew")

        # Right Frame
        frm_battary.grid(row=0, column=0, sticky="nsew")
        frm_basic_control.grid(row=1, column=0, sticky="nsew")
        frm_special_control.grid(row=2, column=0, sticky="nsew")
        frm_reset_control.grid(row=3, column=0, sticky="nsew")
        frm_vision_control.grid(row=4, column=0, sticky="nsew")
        frm_fine_control.grid(row=5, column=0, sticky="nsew")

        frm_left.grid(row=0, column=0, sticky="nsew")
        frm_right.grid(row=0, column=1, sticky="nsew")
        self.frms = GUIFrames(
            pb_battery=pb_battery,
            lbl_battery_percentage=self.lbl_battery_percentage,
            frm_nav_vx=frm_nav_vx,
            frm_nav_vy=frm_nav_vy,
            frm_nav_vz=frm_nav_vz,
            btn_connect=btn_connect,
            btn_video_stream=btn_video_stream,
            lbl_count=lbl_count,
            btn_control_gesture=btn_control_gesture,
        )

    def on_crowd(self) -> None:
        """Start crowd control"""
        self.is_crowdcount = True

    def off_crowd(self) -> None:
        """Stop crowd control"""
        self.is_crowdcount = False

    def on_gesture(self) -> None:
        """Open gesture control"""
        self.models_choice.set("None")
        self.is_crowdcount = False
        self.on_stream()
        if self.gesture_thread:
            self.gesture_thread.resume()
            return

        self.gesture_thread = GestureThread(self.gesture_feed, "archery.mp4")
        self.gesture_thread.start()

    def off_gesture(self) -> None:
        """Close gesture control"""
        if self.gesture_thread is None:
            return
        self.gesture_thread.stop()

    def on_drone_connect(self, _):
        """Event handler for drone connection"""
        self.drone.connect()  # connect drone
        self.drone.set_config(activate_gps=True, activate_navdata=True)

        # change connect button color
        self.frms.btn_connect["text"] = "Connected"
        self.frms.btn_connect["background"] = cfg.GREEN_COLOR
        self.frms.btn_connect["foreground"] = cfg.WHITE_COLOR
        self.frms.btn_connect["activebackground"] = cfg.RED_COLOR
        self.frms.btn_connect["activeforeground"] = cfg.WHITE_COLOR

        # set navdata handler as callback
        self.drone.set_callback(self.on_navdata)

    def on_navdata(self, navdata: dict):
        """Callback handler to retrieve navdata from drone instance

        Args:
            navdata (dict): navigation data dictionary
        """
        if not self.drone.is_connected:
            return

        self.opt.navdata = navdata

    def on_stream(self):
        """Event handler for pressing on stream button"""
        if self.drone.video_thread is not None:
            self.on_change_stream_model()
            return

        _LOG.info("Current Model: %s", self.models_choice.get())
        close_stream_callback = idle
        operation_callback = self.update_frame
        self.drone.connect_video(
            close_stream_callback, operation_callback, self.models_choice.get()
        )
        self.frms.btn_video_stream["text"] = "change"

    def on_change_stream_model(self) -> None:
        """Handler for changing the inference model"""
        if self.drone.video_thread is None:
            err_message = "Video thread called before initialized"
            _LOG.error(err_message)
            raise ValueError(err_message)

        _LOG.info("Current Model: %s", self.models_choice.get())
        self.drone.video_thread.change_model(self.models_choice.get())

    def update_frame(self, output_image: np.ndarray, frame: np.ndarray) -> None:
        """Update camera feed output_image

        Args:
            output_image (np.ndarray): output_image data
            frame (np.ndarray): frame data
        """
        if self.is_crowdcount and self.crowd_tick % CROWD_TOCKS == 0:
            density_map = self.crowd_model.predict(frame)
            et_count = int(np.sum(density_map))
            self.frms.lbl_count["text"] = str(et_count)

        self.crowd_tick += 1

        output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
        output_image = cv2.resize(output_image, (400, 380))
        output_image = Image.fromarray(output_image)
        output_image = ImageTk.PhotoImage(output_image)
        self.camera_feed.configure(image=output_image)
        self.camera_feed.image = output_image

    def __call__(self) -> None:
        """Run the GUI window"""
        empty_frame = np.zeros((400, 380, 3), dtype=np.uint8)
        self.update_frame(empty_frame, empty_frame)
        self.on_stream()
        self.window.mainloop()

    def on_close_window(self):
        """Event handler for closing the GUI window

        It stop the drone connection and destroyes and GUI window
        """
        if self.opt.plot_job is None:
            err_message = "GUI closed before initialized"
            _LOG.critical(err_message)
            raise AssertionError(err_message)

        if self.gesture_thread:
            self.gesture_thread.stop()

        self.drone.stop()
        self.window.after_cancel(self.opt.plot_job)
        self.opt.plot_job = None
        plt.close()
        self.window.destroy()
        _LOG.info("GUI closed")


def idle() -> None:
    """Idle function"""


def to_angle(value: float, max_value: float) -> float:
    """Convert a value ration to an angle"""
    angle = (value / max_value) * cfg.MAX_ANGLE
    return angle
