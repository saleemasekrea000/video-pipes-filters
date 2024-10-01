import cv2
import numpy as np
from video_pipeline.filters.base_filter import Filter


class BrightGaussianNoiseFilter(Filter):
    def __init__(self, input_queue, output_queue, mean=10, sigma=5):
        super().__init__(input_queue, output_queue)
        self.mean = mean
        self.sigma = sigma

    def apply_filter(self, frame, timestamp):
        print("bright gaussian noise filter", timestamp, "ms")
        noise = np.random.normal(self.mean, self.sigma, frame.shape).astype(np.uint8)
        noisy_frame = cv2.add(frame, noise)
        return noisy_frame
