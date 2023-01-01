from typing import Optional, Union
from dronevis.abstract import CVModel
from threading import Thread
import cv2
import random
import time
from typing import Callable
from dronevis.utils import write_fps


class DemoDrone:
    """Demo class for running ``demo GUI``."""

    def __init__(
        self,
        ip: str = "192.168.1.1",
    ) -> None:
        """Construct demo object"""

        self.is_connected = False
        self.nav_thread = None
        self.video_thread = None

    def connect_video(self, callback: Callable, model: CVModel) -> None:

        if not hasattr(callable, "__call__"):
            raise TypeError("Need a function")

            # if not isinstance(model, CVModel):
            #     raise TypeError("Please provide a model of type ``CVModel``")
        self.video_thread = DemoVideoThread(callback, model)
        self.video_thread.start()

    def disconnect_video(self):
        if self.video_thread is None:
            raise ValueError("Video is not initialized")

        self.video_thread.stop()
        time.sleep(0.2)
        self.video_thread = None

    def connect(self) -> None:
        print("Drone connected")
        self.is_connected = True

    def set_callback(self, callback: Optional[Callable] = None) -> None:
        if callback == None:
            callback = self.print_navdata

        if not hasattr(callback, "__call__"):
            raise TypeError("Need a function")

        if self.nav_thread == None:
            self.nav_thread = DemoNavThread(callback)
            self.nav_thread.start()
        else:
            self.nav_thread.change_callback(callback)
            self.nav_thread.start()

    def set_config(self, activate_gps=True, activate_navdata=True):
        pass

    def print_navdata(self, navdata: dict) -> None:
        print(navdata)

    def takeoff(self):
        print("takeoff")

    def land(self):
        print("land")

    def calibrate(self):
        print("calibrate")

    def forward(self):
        print("forward")

    def backward(self):
        print("backward")

    def left(self):
        print("left")

    def right(self):
        print("right")

    def up(self):
        print("up")

    def down(self):
        print("down")

    def rotate_left(self):
        print("rotate_left")

    def rotate_right(self):
        print("rotate_right")

    def hover(self):
        print("hover")

    def emergency(self):
        print("emergency")

    def stop(self):
        self.is_connected = False
        if self.video_thread is not None:
            self.video_thread.stop()
            self.video_thread.join()

        if self.nav_thread is not None:
            self.nav_thread.stop()
            self.nav_thread.join()

    def reset(self):
        print("reset")


class DemoVideoThread(Thread):
    def __init__(
        self,
        close_callback: Callable,
        model: CVModel,
        video_index: Union[str, int] = 0,
        frame_name: str = "Demo Video Capture",
    ) -> None:

        super(DemoVideoThread, self).__init__()
        self.close_callback = close_callback
        self.model = model
        self.frame_name = frame_name
        self.video_index = video_index
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            raise ValueError("Cannot read video stream")
        
        prev_time = 0
        while cap.isOpened():
            if not self.running:
                break
            
            _, frame = cap.read()
            
            frame = self.model.predict(frame)
            cur_time = time.time()
            fps = 1 / (cur_time - prev_time)
            prev_time = cur_time
            cv2.imshow(self.frame_name, write_fps(frame, fps))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print("Closing Video Stream ...")
        cap.release()
        cv2.destroyAllWindows()
        self.close_callback()
        
    def change_model(self, model):
        self.model = model

    def stop(self):
        self.running = False


class DemoNavThread(Thread):
    def __init__(self, callback=None):
        super(DemoNavThread, self).__init__()
        self.callback = callback
        self.running = True

    def change_callback(self, new_callback: Callable) -> bool:
        if not hasattr(new_callback, "__call__"):
            return False

        self.callback = new_callback
        return True

    def run(self):
        vx, vy, vz, h = [0.0] * 4
        battery = random.randint(0, 100)
        while self.running:

            mov_avg = lambda old, new: old * 0.9 + new * 0.1
            vx = mov_avg(vx, random.uniform(0, 2000))
            vy = mov_avg(vy, random.uniform(0, 2000))
            vz = mov_avg(vz, random.uniform(0, 2000))
            h = mov_avg(h, random.uniform(0, 50000))

            data = {
                "navdata_demo": {
                    "battery_percentage": battery,
                    "vx": vx,
                    "vy": vy,
                    "vz": vz,
                    "altitude": h,
                },
            }
            assert self.callback, "Please provide a callback"
            self.callback(data)
            time.sleep(0.05)

    def stop(self):
        self.running = False
        print("Closing Nav Thread ...")
