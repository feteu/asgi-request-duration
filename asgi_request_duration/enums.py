from enum import Enum

class TimeGranularity(Enum):
    NANOSECONDS = 1e9
    MICROSECONDS = 1e6
    MILLISECONDS = 1e3
    SECONDS = 1.0
