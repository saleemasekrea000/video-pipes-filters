# useful resource
# https://learn.microsoft.com/en-us/azure/architecture/patterns/pipes-and-filters
# [BCK13].
import queue
import threading
from video_capture import VideoCapture
from frame_displayer import FrameDisplay
from video_pipeline.filters.black_and_white import BlackAndWhiteFilter
from video_pipeline.filters.mirror import MirrorFilter
from video_pipeline.filters.resize import ResizeFilter
from video_pipeline.filters.bright import BrightGaussianNoiseFilter


def main():
    queues = [queue.Queue() for _ in range(5)]

    # Start video capture from a file
    # video_url = "resources/vv.mp4"
    video_url =0
    video_capture = VideoCapture(queues[0], video_url)
    capture_thread = threading.Thread(target=video_capture.run)
    capture_thread.start()

    filters = [
        BlackAndWhiteFilter(queues[0], queues[1]),
        MirrorFilter(queues[1], queues[2]),
        ResizeFilter(queues[2], queues[3]),
        BrightGaussianNoiseFilter(queues[3], queues[4]),
    ]

    filter_threads = []
    for filter_ in filters:
        thread = threading.Thread(target=filter_.run)
        thread.start()
        filter_threads.append(thread)

    # Start displaying frames
    display = FrameDisplay(queues[0], queues[4])
    display_thread = threading.Thread(target=display.run)
    display_thread.start()

    capture_thread.join()

    for thread in filter_threads:
        thread.join()

    display_thread.join()


if __name__ == "__main__":
    main()
