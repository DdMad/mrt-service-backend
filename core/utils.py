import datetime
from typing import Any, List, Tuple

from app.core.config import settings


def convert_time_range_to_minute_range(time_range: Tuple[str, str]) -> List[Tuple[int, int]]:
    '''
    Convert tuple of time range string to tuple of minutes.
    E.g. 1. (10:00, 12:00) -> [(600, 720)]
    E.g. 2. (20:00, 04:00) -> [(1200, 1440), (0, 240)]
    '''
    start = time_range[0].split(':')
    end = time_range[1].split(':')

    start_hour = int(start[0])
    start_minute = int(start[1])
    end_hour = int(end[0])
    end_minute = int(end[1])

    if start_hour > end_hour or (start_hour == end_hour and start_minute > end_minute):
        return [(start_hour * 60 + start_minute, 24 * 60), (0, end_hour * 60 + end_minute)]
    return [(start_hour * 60 + start_minute, end_hour * 60 + end_minute)]


def convert_string_to_time(time_str: str) -> datetime.datetime:
    '''
    Convert date time string to datetime.
    '''
    return datetime.datetime.strptime(time_str, settings.TIME_FORMAT)

def convert_path_to_steps(path: List[str], estimate: int=None) -> List[str]:
    '''
    Convert path to human readable steps.
    E.g. ['EW1', 'EW2', 'EW3', 'EW4', 'CG0', 'CG1'] will be converted to
    [
        'Take EW from EW1 Pasir Ris to EW4 Tanah Merah',
        'Change EW to CG',
        'Take CG from CG0 to CG1',
        'In total it takes 5 stops'
    ]
    '''
    start = None
    prev = None
    steps = []
    for station in path:
        if start is None:
            start = station
        else:
            if station.line != start.line:
                steps.append(f'Take {start.line} from {start.id} {start.name} to {prev.id} {prev.name}')
                steps.append(f'Change {start.line} to {station.line}')
                start = station
        prev = station
    end = path[-1]
    if end.line == start.line and end.id != start.id:
        steps.append(f'Take {start.line} from {start.id} {start.name} to {prev.id} {prev.name}')
    if estimate is not None:
        steps.append(f'Done! Reach {end.id} {end.name}. The total estimated time is {estimate} minutes')
    else:
        steps.append(f'Done! Reach {end.id} {end.name}. In total it takes {len(path) - 1} stops')
    return steps
