import datetime

from app.core.utils import (convert_path_to_steps, convert_string_to_time,
                            convert_time_range_to_minute_range)
from app.services.mrt_service import Station


def test_convert_time_range_to_minute_range():
    assert convert_time_range_to_minute_range(('10:00', '12:00')) == [(600, 720)]
    assert convert_time_range_to_minute_range(('20:00', '04:00')) == [(1200, 1440), (0, 240)]

def test_convert_string_to_time():
    assert convert_string_to_time('2021-03-29T10:00') == datetime.datetime(2021, 3, 29, 10, 0)

def test_convert_path_to_steps():
    path = [
        Station('NS1', 'Jurong East', ''),
        Station('EW24', 'Jurong East', ''),
        Station('EW23', 'Clementi', ''),
        Station('EW22', 'Dover', ''),
        Station('EW21', 'Buona Vista', ''),
        Station('CC22', 'Buona Vista', ''),
        Station('CC21', 'Holland Village', ''),
        Station('CC20', 'Farrer Road', ''),
        Station('CC19', 'Botanic Gardens', ''),
        Station('CC17', 'Caldecott', ''),
        Station('CC16', 'Marymount', ''),
        Station('CC15', 'Bishan', ''),
        Station('NS17', 'Bishan', ''),
        Station('NS16', 'Ang Mo Kio', ''),
    ]
    estimated_time = 147
    expected = [
        "Take NS from NS1 Jurong East to NS1 Jurong East",
        "Change NS to EW",
        "Take EW from EW24 Jurong East to EW21 Buona Vista",
        "Change EW to CC",
        "Take CC from CC22 Buona Vista to CC15 Bishan",
        "Change CC to NS",
        "Take NS from NS17 Bishan to NS16 Ang Mo Kio",
        "In total it takes 13 stops"
    ]
    expected_with_estimate = [
        "Take NS from NS1 Jurong East to NS1 Jurong East",
        "Change NS to EW",
        "Take EW from EW24 Jurong East to EW21 Buona Vista",
        "Change EW to CC",
        "Take CC from CC22 Buona Vista to CC15 Bishan",
        "Change CC to NS",
        "Take NS from NS17 Bishan to NS16 Ang Mo Kio",
        "The total estimated time is 147 minutes"
    ]
    assert convert_path_to_steps(path) == expected
    assert convert_path_to_steps(path, estimated_time) == expected_with_estimate
