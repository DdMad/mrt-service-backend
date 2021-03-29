from fastapi import FastAPI
from .services.mrt_service import MrtService


app = FastAPI()


@app.get("/")
async def root():
    mrt_map = MrtService()
    paths = mrt_map.find_route_by_stop('EW1', 'CC1')
    result = []
    for path in paths:
        result.append(str([s.id for s in path]))
    return result
