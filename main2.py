import queue
import threading
import signal
import sys
from video_capture import VideoCapture
from frame_displayer import FrameDisplay
from video_pipeline.filters.black_and_white import BlackAndWhiteFilter
from video_pipeline.filters.mirror import MirrorFilter
from video_pipeline.filters.resize import ResizeFilter
from video_pipeline.filters.bright import BrightGaussianNoiseFilter

threads = []  # Global list to store all threads

def signal_handler(sig, frame):
    """Handle keyboard interrupt (Ctrl+C)."""
    print("\nKeyboard interrupt received. Terminating all threads...")
    for thread in threads:
        if thread.is_alive():
            thread.join(timeout=1)
    sys.exit(0)

def main(video_url, display):
    global threads

    # Register the keyboard interrupt signal handler
    signal.signal(signal.SIGINT, signal_handler)

    queues = [queue.Queue() for _ in range(5)]

    # Start video capture from the specified source
    video_capture = VideoCapture(queues[0], video_url)
    capture_thread = threading.Thread(target=video_capture.run, daemon=True)
    capture_thread.start()
    threads.append(capture_thread)

    filters = [
        BlackAndWhiteFilter(queues[0], queues[1]),
        MirrorFilter(queues[1], queues[2]),
        ResizeFilter(queues[2], queues[3]),
        BrightGaussianNoiseFilter(queues[3], queues[4]),
    ]

    for filter_ in filters:
        thread = threading.Thread(target=filter_.run, daemon=True)
        thread.start()
        threads.append(thread)

    if display:
        # Start displaying frames
        display = FrameDisplay(queues[0], queues[4])
        display_thread = threading.Thread(target=display.run, daemon=True)
        display_thread.start()
        threads.append(display_thread)
    else:
        # Consume frames without displaying
        def consume_frames(q):
            while True:
                item = q.get()
                if item is None:
                    break

        original_consumer = threading.Thread(target=consume_frames, args=(queues[0],), daemon=True)
        filtered_consumer = threading.Thread(target=consume_frames, args=(queues[4],), daemon=True)
        original_consumer.start()
        filtered_consumer.start()
        threads.append(original_consumer)
        threads.append(filtered_consumer)

    # Wait for all threads to complete
    for thread in threads:
        if thread.is_alive():
            thread.join(timeout=1)
            print("Thread", thread.name, "completed.")
    sys.exit(0)
        
    
        

    print("Processing completed. Exiting program.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Video processing pipeline.")
    parser.add_argument("--video", type=str, default=0, help="Video source (default: 0 for webcam)")
    parser.add_argument("--display", action="store_true", help="Display the video output")
    args = parser.parse_args()

    main(args.video, args.display)
