from app.core.utils import convert_string_to_time
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

    def test_find_route_by_route(self):
        service = self.__class__.mrt_service