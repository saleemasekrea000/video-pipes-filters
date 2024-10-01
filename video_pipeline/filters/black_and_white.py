import cv2

from video_pipeline.filters.base_filter import Filter


class BlackAndWhiteFilter(Filter):
    def apply_filter(self, frame):
        print("applying BlackAndWhiteFilter")
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
