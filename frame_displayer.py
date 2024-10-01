import cv2


class FrameDisplay:
    def __init__(self, original_queue, filtered_queue):
        self.original_queue = original_queue
        self.filtered_queue = filtered_queue

    def run(self):
        while True:
            original_item = self.original_queue.get()
            filtered_item = self.filtered_queue.get()

            if original_item is None or filtered_item is None:
                break

            _, original_frame = original_item
            _, filtered_frame = filtered_item

            cv2.imshow("Input", original_frame)
            cv2.imshow("Output", filtered_frame)

            if cv2.waitKey(20) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()
