from math import ceil  # noqa
from datetime import datetime, timedelta
import pytz


# def round_to_next_15(timestamp: datetime, delta: timedelta = timedelta(minutes=15)):
#     return datetime.min + ceil((timestamp - datetime.min) / delta) * delta


def round_to_next_15(timestamp: datetime):
    minutes = timestamp.min
    increase_hour = False
    if timestamp.minute >= 45:
        minutes = 0
        increase_hour = True
    elif timestamp.minute >= 30:
        minutes = 45
    elif timestamp.minute >= 15:
        minutes = 30
    else:
        minutes = 15
    resp = datetime(
        year=timestamp.year,
        month=timestamp.month,
        day=timestamp.day,
        hour=timestamp.hour,
        minute=minutes,
        second=0,
        tzinfo=timestamp.tzinfo,
    )
    if increase_hour:
        resp = resp + timedelta(hours=1)
    return resp


def back_to_15(timestamp: datetime):
    """Roll back a given timestamp to 15 minute round"""
    if timestamp.minute >= 45:
        _min = 45
    elif timestamp.minute >= 30:
        _min = 30
    elif timestamp.minute >= 15:
        _min = 15
    else:
        _min = 0
    return datetime(
        year=timestamp.year,
        month=timestamp.month,
        day=timestamp.day,
        hour=timestamp.hour,
        minute=_min,
        second=0,
        tzinfo=timestamp.tzinfo,
    )


def to_pydatetime(timestamp: datetime):
    return datetime(
        year=timestamp.year,
        month=timestamp.month,
        day=timestamp.day,
        hour=timestamp.hour,
        minute=timestamp.minute,
        second=timestamp.second,
        tzinfo=timestamp.tzinfo,
    )


def time_to_timezone(utc_time, tzone):
    target_timezone = pytz.timezone(tzone)
    converted_time = target_timezone.normalize(
        pytz.utc.localize(datetime.combine(datetime.today(), utc_time)).astimezone(
            target_timezone
        )
    ).time()
    return converted_time
