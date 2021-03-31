import pytest
from app.core.utils import convert_string_to_time
from app.exceptions.invalid_input_exception import InvalidInputException
from app.services.mrt_service import MrtService


class TestMrtService:
    @classmethod
    def setup_class(cls):
        cls.mrt_service = MrtService()

    def test_get_transport_time(self):
        service = self.__class__.mrt_service
        assert service.get_transport_time(service.station_mapping['EW1'], service.station_mapping['EW2'], convert_string_to_time('2021-03-30T08:00')) ==  10
        assert service.get_transport_time(service.station_mapping['NS1'], service.station_mapping['NS2'], convert_string_to_time('2021-03-30T08:00')) ==  12
        assert service.get_transport_time(service.station_mapping['NS1'], service.station_mapping['EW24'], convert_string_to_time('2021-03-30T08:00')) ==  15

    def test_is_peak_hours(self):
        service = self.__class__.mrt_service
        assert service.is_in_peak_hours(convert_string_to_time('2021-03-30T06:00')) == True
        assert service.is_in_peak_hours(convert_string_to_time('2021-03-30T08:00')) == True
        assert service.is_in_peak_hours(convert_string_to_time('2021-03-30T18:00')) == True
        assert service.is_in_peak_hours(convert_string_to_time('2021-03-30T19:00')) == True
        assert service.is_in_peak_hours(convert_string_to_time('2021-03-30T09:00')) == False
        assert service.is_in_peak_hours(convert_string_to_time('2021-03-30T21:00')) == False
        assert service.is_in_peak_hours(convert_string_to_time('2021-03-30T12:00')) == False
        assert service.is_in_peak_hours(convert_string_to_time('2021-03-28T08:00')) == False
        assert service.is_in_peak_hours(convert_string_to_time('2021-03-28T13:00')) == False

    def test_is_night_hours(self):
        service = self.__class__.mrt_service
        assert service.is_in_night_hours(convert_string_to_time('2021-03-30T22:00')) == True
        assert service.is_in_night_hours(convert_string_to_time('2021-03-30T00:00')) == True
        assert service.is_in_night_hours(convert_string_to_time('2021-03-30T04:00')) == True
        assert service.is_in_night_hours(convert_string_to_time('2021-03-30T06:00')) == False
        assert service.is_in_night_hours(convert_string_to_time('2021-03-28T08:00')) == False
        assert service.is_in_night_hours(convert_string_to_time('2021-03-28T13:00')) == False

    def test_find_route_by_stop(self):
        service = self.__class__.mrt_service
        origin = 'NS1'
        destination = 'NS16'
        assert [s.id for s in service.find_route_by_stop(origin, destination)] == ['NS1', 'EW24', 'EW23', 'EW22', 'EW21', 'CC22', 'CC21', 'CC20', 'CC19', 'CC17', 'CC16', 'CC15', 'NS17', 'NS16']

        with pytest.raises(InvalidInputException):
            service.find_route_by_stop('NS88', 'NS99')

    def test_find_route_by_time(self):
        service = self.__class__.mrt_service
        origin = 'NS1'
        destination = 'NS16'
        (time, path) = service.find_route_by_time(origin, destination, '2021-03-30T08:00')
        assert [s.id for s in path] == ['NS1', 'EW24', 'EW23', 'EW22', 'EW21', 'CC22', 'CC21', 'CC20', 'CC19', 'CC17', 'CC16', 'CC15', 'NS17', 'NS16']
        assert time == 147

        with pytest.raises(InvalidInputException):
            service.find_route_by_time('NS88', 'NS99', '2021-03-30T08:00')
        with pytest.raises(InvalidInputException):
            service.find_route_by_time('DT1', 'DT2', '2021-03-30T04:00')
