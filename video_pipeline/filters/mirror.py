import cv2

from video_pipeline.filters.base_filter import Filter


class MirrorFilter(Filter):
    def apply_filter(self, frame, timestamp):
        print("mirror filter", timestamp, "ms")
        return cv2.flip(frame, 1)
