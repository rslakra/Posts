#
# Author: Rohtash Lakra
#
import time
from datetime import datetime
from typing import Any, Union


def now() -> float:
    """Returns current time as float."""
    return time.time()


@staticmethod
def nowMillis() -> int:
    """Returns current time in milliseconds."""
    return int(StopWatch.now() * 1000)


class StopWatch(object):
    """Test support functionality for other tests."""
    
    def __init__(self):
        self.start_time = None
        self.duration = None
    
    @classmethod
    def now(cls) -> float:
        """Returns current time as float."""
        return time.time()
    
    def start(self):
        self.start_time = self.now()
        self.duration = None
    
    def stop(self):
        self.duration = self.now() - self.start_time
    
    # @property
    def elapsed(self):
        assert self.start_time is not None
        return self.now() - self.start_time
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


class TimeUtils:
    
    @classmethod
    def nowMillis(cls) -> int:
        """Returns current time in milliseconds."""
        return int(time.time() * 1000)
    
    @classmethod
    def format_datetime(cls, timestamp_obj) -> Union[str, Any]:
        if isinstance(timestamp_obj, datetime):
            return timestamp_obj.isoformat()
        elif isinstance(timestamp_obj, dict):
            return {key: cls.format_datetime(value) for key, value in timestamp_obj.items()}
        elif isinstance(timestamp_obj, list):
            return [cls.format_datetime(item) for item in timestamp_obj]
        else:
            return timestamp_obj
