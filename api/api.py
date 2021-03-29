from fastapi import APIRouter
from typing import Any, List
from app.services.mrt_service import mrt_service
from app.core.utils import convert_path_to_steps


router = APIRouter()

@router.get('/find-route-by-stop')
def find_route_by_stop(origin: str, destination: str) -> Any:
    paths = mrt_service.find_route_by_stop(origin, destination)
    response = convert_path_to_steps(paths[0])
    return response


@router.get('/find-route-by-time')
def find_route_by_time(origin: str, destination: str, time: str) -> Any:
    (time, path) = mrt_service.find_route_by_time(origin, destination, time)
    response = convert_path_to_steps(path, estimate=time)
    return response