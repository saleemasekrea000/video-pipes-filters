import cv2
from video_pipeline.filters.base_filter import Filter


class ResizeFilter(Filter):
    def __init__(self, input_queue, output_queue, size=(500, 400)):
        super().__init__(input_queue, output_queue)
        self.size = size

    def apply_filter(self, frame):
        print("applying ResizeFilter")
        return cv2.resize(frame, self.size)
