from collections import deque
import csv
import heapq

from ..core.config import settings
from ..core.utils import convert_time_range_to_minute_range, convert_string_to_time

class MrtService:
    def __init__(self):
        # Get station data from map file
        self.stations = []
        with open(settings.STATION_MAP_FILE_PATH, 'r') as f:
            csvreader = csv.reader(f)
            next(csvreader)
            for row in csvreader:
                self.stations.append(Station(row[0], row[1], row[2]))
        self.__build_normal_station_paths()
        self.__build_interchange_station_paths()

    def __build_normal_station_paths(self):
        # Build path for normal stations
        current_line = self.stations[0].line
        prev_station = None
        self.station_mapping = {}
        for station in self.stations:
            self.station_mapping[station.id] = station
            if station.line == current_line:
                if prev_station:
                    station.next.append(prev_station)
                    prev_station.next.append(station)
            else:
                current_line = station.line
            prev_station = station
        
    def __build_interchange_station_paths(self):
        # Build path for interchange stations
        station_name_id_mapping = {}
        for station in self.stations:
            if station.name not in station_name_id_mapping:
                station_name_id_mapping[station.name] = [station.id]
            else:
                station_name_id_mapping[station.name].append(station.id)
        for k in station_name_id_mapping:
            if len(station_name_id_mapping[k]) > 1:
                stations = station_name_id_mapping[k]
                for id1 in stations:
                    for id2 in stations:
                        if id1 != id2:
                            self.station_mapping[id1].next.append(self.station_mapping[id2])
    
    def is_in_peak_hours(self, time):
        if time.isoweekday() not in settings.PEAK_HOURS_CONFIG['days']:
            return False
        minute_range = []
        for i in settings.PEAK_HOURS_CONFIG['time_range']:
            minute_range.extend(convert_time_range_to_minute_range(i))
        current_minute = time.hour * 60 + time.minute
        for r in minute_range:
            if current_minute in range(r[0], r[1]):
                return True
        return False

    def is_in_night_hours(self, time):
        if time.isoweekday() not in settings.NIGHT_HOURS_CONFIG['days']:
            return False     
        minute_range = []
        for i in settings.NIGHT_HOURS_CONFIG['time_range']:
            minute_range.extend(convert_time_range_to_minute_range(i))
        current_minute = time.hour * 60 + time.minute
        for r in minute_range:
            if current_minute in range(r[0], r[1]):
                return True
        return False

    def get_transport_time(self, current, next, time):
        peak_hour_config = settings.PEAK_HOURS_CONFIG['time_taken']
        night_hour_config = settings.NIGHT_HOURS_CONFIG['time_taken']
        night_hour_unavailable_lines = settings.NIGHT_HOURS_CONFIG['exclude']
        non_peak_hour_config = settings.NON_PEAK_HOURS_CONFIG['time_taken']

        if self.is_in_peak_hours(time):
            if current.line == next.line:
                if current.line in peak_hour_config:
                    return peak_hour_config[current.line]
                else:
                    return peak_hour_config['others']
            else:
                return peak_hour_config['change']
        elif self.is_in_night_hours(time):
            if current.line in night_hour_unavailable_lines or next.line in night_hour_unavailable_lines:
                return -1
            if current.line == next.line:
                if current.line in night_hour_config:
                    return night_hour_config[current.line]
                else:
                    return night_hour_config['others']
            else:
                return night_hour_config['change']
        else:
            if current.line == next.line:
                if current.line in non_peak_hour_config:
                    return non_peak_hour_config[current.line]
                else:
                    return non_peak_hour_config['others']
            else:
                return non_peak_hour_config['change']

    def find_route_by_time(self, origin, destination, start_time):
        start_datetime = convert_string_to_time(start_time)
        origin_station = self.station_mapping[origin]
        visited = set()
        queue = []
        heapq.heappush(queue, (0, [origin_station]))
        while queue:
            (current_time, path) = heapq.heappop(queue)
            current = path[-1]
            if current.id == destination:
                return (current_time, path)
            if current.id in visited:
                continue
            visited.add(current.id)
            for next_station in current.next:
                if next_station.id not in visited:
                    next_path = list(path)
                    next_path.append(next_station)
                    next_time = current_time + self.get_transport_time(next_path[-2], next_path[-1], start_datetime)
                    heapq.heappush(queue, (next_time, next_path))

    def find_route_by_stop(self, origin, destination):
        origin_station = self.station_mapping[origin]
        visited_queue = deque()
        visited_queue.appendleft(set())
        queue = deque()
        queue.appendleft([origin_station])
        paths = []
        while queue:
            path = queue.pop()
            visited = visited_queue.pop()
            current = path[-1]
            if current.id == destination:
                paths.append(path)
                if len(paths) >= 3:
                    break
                else:
                    continue
            if current.id in visited:
                continue
            visited.add(current.id)
            for next_station in current.next:
                if next_station.id not in visited:
                    next_path = list(path)
                    next_path.append(next_station)
                    queue.appendleft(next_path)
                    visited_queue.appendleft(set(visited))
        return paths


class Station:
    def __init__(self, id, name, open_date):
        self.id = id
        self.line = id[:2]
        self.name = name
        self.open_date = open_date
        self.next = []

    def __lt__(self, s2):
        return self.name < s2.name

    def __repr__(self):
        return f'Station({self.id}, {self.name}, {self.open_date}, {self.next})'

    def __str__(self):
        return f'(id:{self.id}, name:{self.name}, open_date:{self.open_date})'

m = MrtService()
(time, path) = m.find_route_by_time('NS1', 'NS16', '2021-03-30T08:00')
print(time)
print([s.id for s in path])
# t = m.get_transport_time(m.station_mapping['EW4'], m.station_mapping['CG0'], convert_string_to_time('2021-03-30T08:00'))
# print(t)