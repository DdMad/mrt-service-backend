import datetime
from .config import settings


def convert_time_range_to_minute_range(time_range):
    start = time_range[0].split(':')
    end = time_range[1].split(':')

    start_hour = int(start[0])
    start_minute = int(start[1])
    end_hour = int(end[0])
    end_minute = int(end[1])

    if start_hour > end_hour or (start_hour == end_hour and start_minute > end_minute):
        return [(start_hour * 60 + start_minute, 24 * 60), (0, end_hour * 60 + end_minute)]
    return [(start_hour * 60 + start_minute, end_hour * 60 + end_minute)]


def convert_string_to_time(time_str):
    return datetime.datetime.strptime(time_str, settings.TIME_FORMAT)