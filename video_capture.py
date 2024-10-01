import cv2
import time


class VideoCapture:
    def __init__(self, input_queue, source=0):
        self.input_queue = input_queue
        self.cap = cv2.VideoCapture(source)

    def run(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame_time = 1.0 / fps

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                # print("failddddddd")
                break

            timestamp = cv2.getTickCount() / cv2.getTickFrequency()
            self.input_queue.put((timestamp, frame))
            # It ensures that frames are read at a rate that matches the original video’s playback speed.
            time.sleep(frame_time)

        self.cap.release()
        self.input_queue.put(None)
