from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'

    STATION_MAP_FILE_PATH: str = 'app/StationMap.csv'

    TIME_FORMAT: str = '%Y-%m-%dT%H:%M'

    PEAK_HOURS_CONFIG: dict = {
        'time_range': [('06:00','09:00'), ('18:00', '21:00')],
        'days': [1,2,3,4,5],
        'time_taken': {
            'NS': 12,
            'NE': 12,
            'others': 10,
            'change': 15,
        },
        'exclude': [],
    }

    NIGHT_HOURS_CONFIG: dict = {
        'time_range': [('22:00','06:00')],
        'days': [1,2,3,4,5,6,7],
        'time_taken': {
            'TE': 8,
            'others': 10,
            'change': 10,
        },
        'exclude': ['DT', 'CG', 'CE'],
    }

    NON_PEAK_HOURS_CONFIG: dict = {
        'time_range': [],
        'days': [1,2,3,4,5,6,7],
        'time_taken': {
            'DT': 8,
            'TE': 8,
            'others': 10,
            'change': 10,
        },
        'exclude': [],
    }

settings = Settings()