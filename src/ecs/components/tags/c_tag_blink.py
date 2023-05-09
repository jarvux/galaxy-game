import time
class CTagBlink:
    def __init__(self, interval):
        self.timestamp = time.time()
        self.interval = interval