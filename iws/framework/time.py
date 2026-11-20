#
# Author: Rohtash Lakra
#
import time


def now() -> float:
    """Returns current time as float."""
    return time.time()


def timeMillis() -> int:
    """Returns current time in milliseconds."""
    return int(time.time() * 1000)


class StopWatch(object):
    """Test support functionality for other tests."""

    def __init__(self):
        self.start_time = None
        self.duration = None

    def start(self):
        self.start_time = self.now()
        self.duration = None

    def stop(self):
        self.duration = self.now() - self.start_time

    @staticmethod
    def now():
        return time.time()

    # @property
    def elapsed(self):
        assert self.start_time is not None
        return self.now() - self.start_time

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
