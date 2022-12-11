from tkinter import *
from tkinter.ttk import *
from dronevis.gui.configs import *
from dronevis.gui.image_button import ImageButton
from dronevis.gui.main_button import MainButton

def main():
    window = Tk()
    window.geometry("1000x540")
    s = Style()
    s.theme_use("clam")
    s.configure(".", font=MAIN_FONT, background=MAIN_COLOR, foreground=WHITE_COLOR)
    s.configure("MainFrame.TFrame", relief="solid", borderwidth=1)
    s.configure(
        "Custom.Horizontal.TProgressbar", troughcolor=WHITE_COLOR, background=GREEN_COLOR
    )
    window.title("Drone Vision")

    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, minsize=600, weight=1)
    window.columnconfigure(1, minsize=330, weight=1)

    frm_left = Frame(master=window)
    frm_right = Frame(master=window)

    # Left Configs
    frm_left.rowconfigure(0, minsize=440, weight=1)
    frm_left.rowconfigure(1, minsize=100, weight=1)
    frm_left.columnconfigure(0, minsize=600, weight=1)

    # Right Configs
    frm_right.columnconfigure(0, minsize=400, weight=1)
    frm_right.rowconfigure(0, minsize=260, weight=1)
    frm_right.rowconfigure(1, minsize=180, weight=1)
    frm_right.rowconfigure(2, minsize=100, weight=1)

    frm_info = Frame(master=frm_left)
    frm_info.rowconfigure(0, weight=1)
    frm_info.rowconfigure(1, weight=2)
    frm_info.rowconfigure(2, weight=2)
    frm_info.columnconfigure(0, weight=1)

    ######################## Battary Data ###################################
    frm_battary = Frame(frm_info, style="MainFrame.TFrame")
    lbl_battary = Label(frm_battary, text="Battery Percentage", font=HEADER_FONT)
    frm_progress = Frame(frm_battary)
    pb_battery = Progressbar(
        frm_progress,
        mode="determinate",
        length=300,
        maximum=100,
        orient=HORIZONTAL,
        value=67,
        style="Custom.Horizontal.TProgressbar",
    )
    lbl_battery_percentage = Label(frm_progress, text="67%")

    frm_battary.rowconfigure(0, weight=1)
    frm_battary.rowconfigure(2, weight=1)
    frm_battary.columnconfigure(0, weight=1)

    ######################## Basic Control ##################################
    frm_basic_control = Frame(master=frm_right, style="MainFrame.TFrame")
    lbl_basic_control = Label(frm_basic_control, text="Basic Control", font=HEADER_FONT)

    btn_forward = ImageButton(
        frm_basic_control,
        title="FORWARD",
        message="Move the drone forward",
        img="forward.png",
        size=VERTICAL_ARROW_SIZE,
    )
    btn_backward = ImageButton(
        frm_basic_control,
        title="BACKWARD",
        message="Move the drone Backword",
        img="backward.png",
        size=VERTICAL_ARROW_SIZE,
    )
    btn_right = ImageButton(
        frm_basic_control,
        title="RIGHT",
        message="Move the drone to the right",
        img="right.png",
        size=HORIZONTAL_ARROW_SIZE,
    )
    btn_left = ImageButton(
        frm_basic_control,
        title="LFET",
        message="Move the drone to the left",
        img="left.png",
        size=HORIZONTAL_ARROW_SIZE,
    )
    btn_rotate_l = ImageButton(
        frm_basic_control,
        title="ROT L",
        message="Rotate the drone to the left",
        img="rotate_ccw.png",
        size=(35, 30),
    )
    btn_rotate_r = ImageButton(
        frm_basic_control,
        title="ROT R",
        message="Rotate the drone to the right",
        img="rotate_cw.png",
        size=(35, 30),
    )
    btn_up = ImageButton(
        frm_basic_control,
        title="UPWARD",
        message="Move the drone up",
        img="up.png",
        size=VERTICAL_ARROW_SIZE,
    )
    btn_down = ImageButton(
        frm_basic_control,
        title="DOWN",
        message="Move the drone down",
        img="down.png",
        size=VERTICAL_ARROW_SIZE,
    )
    btn_connect = ImageButton(
        frm_basic_control,
        title="CONNECT",
        message="Connect to the drone",
        img="connect.png",
        size=(40, 40),
        is_inverted=True,
    )


    for i in range(4):
        frm_basic_control.rowconfigure(i, weight=1)
        frm_basic_control.columnconfigure(i % 3, minsize=70, weight=1)

    ######################## Special Control #################################
    frm_special_control = Frame(master=frm_right, style="MainFrame.TFrame")
    lbl_special_control = Label(
        frm_special_control, text="Special Control", font=HEADER_FONT
    )
    btn_take_off = MainButton(
        frm_special_control,
        message="The drone takes off the ground",
        text="Take off",
    )
    btn_land = MainButton(
        frm_special_control,
        message="The drone lands smoothly",
        text="Land",
    )
    btn_hover = MainButton(
        frm_special_control,
        message="The drone hovers in its position",
        text="Hover",
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
    lbl_reset_control = Label(frm_reset_control, text="Reset Control", font=HEADER_FONT)
    btn_reset = MainButton(
        frm_reset_control,
        text="Reset",
        message="Reset drone states. Use it when a red led turns on",
    )
    btn_calib = MainButton(
        frm_reset_control,
        text="Caliberate",
        message="Caliberate drone sensors",
    )
    btn_emerg = MainButton(
        frm_reset_control,
        text="Emergency",
        message="Set drone in emergency state",
    )

    for i in range(3):
        frm_reset_control.rowconfigure(i % 2, weight=1)
        frm_reset_control.columnconfigure(i, minsize=70, weight=1)

    ######################## Vision Control ##################################
    frm_vision_control = Frame(master=frm_left, style="MainFrame.TFrame")
    lbl_vision_control = Label(frm_vision_control, text="Vision Control", font=HEADER_FONT)
    btn_record_video = MainButton(
        master=frm_vision_control,
        text="Record",
        message="Record a video which will be saved on drone controller memory",
    )
    btn_detection = MainButton(
        frm_vision_control,
        text="Detect",
        message="Run object detection algoritm",
    )
    btn_video_stream = MainButton(
        frm_vision_control,
        text="Stream",
        message="Initiate video stream from drone",
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
    lbl_battery_percentage.pack(side=LEFT, padx=5)
    frm_progress.grid(row=2, column=0)

    # vision control
    lbl_vision_control.grid(row=0, column=1, pady=10)
    btn_record_video.grid(row=1, column=0, sticky="ew", padx=10, pady=10, ipady=2)
    btn_detection.grid(row=1, column=1, sticky="ew", padx=10, pady=10, ipady=2)
    btn_video_stream.grid(row=1, column=2, sticky="ew", padx=10, pady=10, ipady=2)

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

    window.mainloop()
