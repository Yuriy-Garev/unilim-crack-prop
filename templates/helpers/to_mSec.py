from datetime import datetime


def ToMSec(time: datetime) -> float:
    """Convert datetime to mSec"""
    testTH = time.hour * 60 * 60 * 1000
    testTM = time.minute * 60 * 1000
    testTS = time.second * 1000
    testTMs = int(time.microsecond * 0.001)
    return (testTH + testTM + testTS + testTMs)*0.001
