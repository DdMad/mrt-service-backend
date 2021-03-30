from fastapi import APIRouter, Query, Response, status
from typing import Any, List
from app.services.mrt_service import mrt_service
from app.core.utils import convert_path_to_steps
from app.exceptions.invalid_input_exception import InvalidInputException


router = APIRouter()

@router.get('/find-route-by-stop')
def find_route_by_stop(
    response: Response,
    origin: str = Query(None, min_length=3, max_length=4, regex="^[a-zA-Z]{2}[0-9]{1,2}$"),
    destination: str = Query(None, min_length=3, max_length=4, regex="^[a-zA-Z]{2}[0-9]{1,2}$"),
    ) -> Any:
    '''
    Find the route between two stations which has the least stops.
    '''
    try:
        path = mrt_service.find_route_by_stop(origin, destination)
    except InvalidInputException as iie:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return [f'Error: {str(iie)}']
    result = convert_path_to_steps(path)
    return result


@router.get('/find-route-by-time')
def find_route_by_time(
    response: Response,
    origin: str = Query(None, min_length=3, max_length=4, regex="^[a-zA-Z]{2}[0-9]{1,2}$"),
    destination: str = Query(None, min_length=3, max_length=4, regex="^[a-zA-Z]{2}[0-9]{1,2}$"),
    time: str = Query(None, min_length=16, max_length=16, regex="^[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}T[0-9]{1,2}:[0-9]{1,2}$"),
    ) -> Any:
    '''
    Find the route between two stations at given time which takes the least time.
    '''
    try:
        (time, path) = mrt_service.find_route_by_time(origin, destination, time)
    except InvalidInputException as iie:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return [f'Error: {str(iie)}']
    result = convert_path_to_steps(path, estimate=time)
    return result