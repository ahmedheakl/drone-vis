from dronevis.abstract import CVModel
import cv2
import time
import mediapipe as mp


class PoseEstimation(CVModel):
    def __init__(self):
        self.pose_module = mp.solutions.pose
        self.drawer = mp.solutions.drawing_utils

    def load_model(self):
        self.net = self.pose_module.Pose()

    def transform_img(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def predict(self, image):
        image = self.transform_img(image)
        res = self.net.process(image)
        if res.pose_landmarks:
            self.drawer.draw_landmarks(
                image, res.pose_landmarks, self.pose_module.POSE_CONNECTIONS
            )
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def detect_webcam(self, video_index: int=0, window_name="Pose"):
        cap = cv2.VideoCapture(video_index)
        prev_time = 0

        while True:
            _, image = cap.read()
            image = self.predict(image)

            cur_time = time.time()
            fps = 1 / (cur_time - prev_time)
            prev_time = cur_time
            cv2.putText(
                image,
                str(int(fps)),
                (70, 50),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (255, 0, 0),
                3,
            )
            cv2.imshow(window_name, image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()
        cap.release()
