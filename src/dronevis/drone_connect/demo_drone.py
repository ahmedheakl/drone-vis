from typing import Optional, Union
from dronevis.abstract import CVModel
from threading import Thread
import cv2
import random
import time
from typing import Callable
from dronevis.utils import write_fps
import logging
from inspect import getmro


class DemoDrone:
    """Demo class for running ``demo GUI``."""

    def __init__(
        self,
        ip: str = "192.168.1.1",
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """Construct demo object"""

        self.is_connected = False
        self.nav_thread = None
        self.video_thread = None
        
        if logger is None:
            logging.basicConfig(level=logging.DEBUG)
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def connect_video(self, callback: Callable, model: CVModel) -> None:

        if not hasattr(callable, "__call__"):
            self.logger.error("not an instance of a function is provided as a callback")
            raise TypeError("please provide a function as a callback")

        if CVModel not in getmro(type(model)):
            self.logger.error("model provided is not an instance of ``CVModel``")
            raise TypeError("please provide a model of type ``CVModel``")
        
        self.video_thread = DemoVideoThread(callback, model)
        self.video_thread.start()

    def disconnect_video(self):
        if self.video_thread is None:
            self.logger.error("not an instance of a function is provided as a callback")
            raise ValueError("video is not initialized")

        self.video_thread.stop()
        time.sleep(0.2)
        self.video_thread = None
        self.logger.debug("video thread stopped")

    def connect(self) -> None:
        self.logger.info("drone connected")
        self.is_connected = True

    def set_callback(self, callback: Optional[Callable] = None) -> None:
        if callback == None:
            callback = self.print_navdata

        if not hasattr(callable, "__call__"):
            self.logger.error("not an instance of a function is provided as a callback")
            raise TypeError("please provide a function as a callback")

        if self.nav_thread == None:
            self.nav_thread = DemoNavThread(callback, logger=self.logger)
            self.nav_thread.start()
            self.logger.debug("nav thread started")
        else:
            self.nav_thread.change_callback(callback)
            self.nav_thread.start()
            self.logger.debug("changed callback")

    def set_config(self, activate_gps=True, activate_navdata=True):
        pass

    def print_navdata(self, navdata: dict) -> None:
        print(navdata)

    def takeoff(self) -> None:
        self.logger.info("takeoff")

    def land(self) -> None:
        self.logger.info("land")

    def calibrate(self) -> None:
        self.logger.info("calibrate")

    def forward(self) -> None:
        self.logger.info("forward")

    def backward(self) -> None:
        self.logger.info("backward")

    def left(self) -> None:
        self.logger.info("left")

    def right(self) -> None:
        self.logger.info("right")

    def up(self) -> None:
        self.logger.info("up")

    def down(self) -> None:
        self.logger.info("down")

    def rotate_left(self) -> None:
        self.logger.info("rotate_left")

    def rotate_right(self) -> None:
        self.logger.info("rotate_right")

    def hover(self) -> None:
        self.logger.info("hover")

    def emergency(self) -> None:
        self.logger.info("emergency")

    def stop(self):
        self.is_connected = False
        if self.video_thread is not None:
            self.video_thread.stop()
            self.video_thread.join()
            self.logger.debug("video thread stopped")

        if self.nav_thread is not None:
            self.nav_thread.stop()
            self.nav_thread.join()
            self.logger.debug("nav thread stopped")
            
        self.logger.warning("drone disconnected")

    def reset(self):
        self.logger.info("reset")


class DemoVideoThread(Thread):
    def __init__(
        self,
        close_callback: Callable,
        model: CVModel,
        video_index: Union[str, int] = 0,
        frame_name: str = "Demo Video Capture",
        logger: Optional[logging.Logger] = None,
    ) -> None:

        super(DemoVideoThread, self).__init__()
        self.close_callback = close_callback
        self.model = model
        self.frame_name = frame_name
        self.video_index = video_index
        self.running = True
        self.logger = logger
        
        if self.logger is None:
            logging.basicConfig(level=logging.DEBUG)
            self.logger = logging.getLogger(__name__)

            

    def run(self):
        assert self.logger, "please init the logger"
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            self.logger.warning("Error while trying to read video. Please check path again")
        
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

        self.logger.debug("closing Video Stream ...")
        cap.release()
        cv2.destroyAllWindows()
        self.close_callback()
        
    def change_model(self, model):
        assert self.logger, "please init the logger"
        self.model = model
        self.logger.debug("model for video thread changed")

    def stop(self):
        self.running = False


class DemoNavThread(Thread):
    def __init__(self, callback=None, logger: Optional[logging.Logger] = None,):
        super(DemoNavThread, self).__init__()
        self.callback = callback
        self.running = True
        self.logger = logger
        
        if self.logger is None:
            logging.basicConfig(level=logging.DEBUG)
            self.logger = logging.getLogger(__name__)

    def change_callback(self, new_callback: Callable) -> bool:
        
        assert self.logger, "pleases init the logger"
        
        if not hasattr(new_callback, "__call__"):
            self.logger.error("not an instance of a function is provided as a callback")
            raise TypeError("please provide a function for callback")

        self.callback = new_callback
        
        self.logger.debug("nav thread callback changed")
        return True

    def run(self):
        assert self.logger, "please init the logger"
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
            if self.callback is None:
                self.logger.error("no callback provided to nav thread")
                raise ValueError("please provide a callback for nav thread first")
            self.callback(data)
            time.sleep(0.05)
            
        self.logger.debug("closing nav thread ...")
        

    def stop(self):
        self.running = False
