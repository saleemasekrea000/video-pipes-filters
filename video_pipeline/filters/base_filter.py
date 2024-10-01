class Filter:
    def __init__(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue

    def apply_filter(self, frame, timestamp):
        pass

    def run(self):
        while True:
            frame = self.input_queue.get()
            if frame is None:
                self.output_queue.put(None)
                break
            timestamp, frame = frame
            processed_frame = self.apply_filter(frame, timestamp)
            self.output_queue.put((timestamp, processed_frame))
