from app.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_find_route_by_stop():
    response = client.get("/api/v1/find-route-by-stop?origin=NS1&destination=NS16")
    assert response.status_code == 200
    assert response.json() == [
        "Take NS from NS1 Jurong East to NS1 Jurong East",
        "Change NS to EW",
        "Take EW from EW24 Jurong East to EW21 Buona Vista",
        "Change EW to CC",
        "Take CC from CC22 Buona Vista to CC15 Bishan",
        "Change CC to NS",
        "Take NS from NS17 Bishan to NS16 Ang Mo Kio",
        "In total it takes 13 stops"
    ]

def test_find_route_by_stop_invalid_input():
    response = client.get("/api/v1/find-route-by-stop?origin=NS88&destination=NS99")
    assert response.status_code == 400
    assert response.json() == [
        "Error: Station NS88 does not exists"
    ]

    response = client.get("/api/v1/find-route-by-stop?origin=NS1&destination=NS99")
    assert response.status_code == 400
    assert response.json() == [
        "Error: Station NS99 does not exists"
    ]

def test_find_route_by_time():
    response = client.get("/api/v1/find-route-by-time?origin=NS1&destination=NS16&time=2021-03-30T08:00")
    assert response.status_code == 200
    assert response.json() == [
        "Take NS from NS1 Jurong East to NS1 Jurong East",
        "Change NS to EW",
        "Take EW from EW24 Jurong East to EW21 Buona Vista",
        "Change EW to CC",
        "Take CC from CC22 Buona Vista to CC15 Bishan",
        "Change CC to NS",
        "Take NS from NS17 Bishan to NS16 Ang Mo Kio",
        "The total estimated time is 147 minutes"
    ]

def test_find_route_by_time_invalid_input():
    response = client.get("/api/v1/find-route-by-time?origin=NS88&destination=NS99&time=2021-03-30T08:00")
    assert response.status_code == 400
    assert response.json() == [
        "Error: Station NS88 does not exists"
    ]

    response = client.get("/api/v1/find-route-by-time?origin=NS1&destination=NS99&time=2021-03-30T08:00")
    assert response.status_code == 400
    assert response.json() == [
        "Error: Station NS99 does not exists"
    ]
