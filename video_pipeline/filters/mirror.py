import cv2

from video_pipeline.filters.base_filter import Filter


class MirrorFilter(Filter):
    def apply_filter(self, frame):
        print("applying MirrorFilter")
        return cv2.flip(frame, 1)
