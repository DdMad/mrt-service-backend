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
        "Done! Reach NS16 Ang Mo Kio. In total it takes 13 stops"
    ]

def test_find_route_by_stop_with_error():
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
    # Peak hours tests
    response = client.get("/api/v1/find-route-by-time?origin=NS1&destination=NS15&time=2021-03-30T08:00")
    assert response.status_code == 200
    assert response.json() == [
        "Take NS from NS1 Jurong East to NS15 Yio Chu Kang",
        "Done! Reach NS15 Yio Chu Kang. The total estimated time is 156 minutes"
    ]

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
        "Done! Reach NS16 Ang Mo Kio. The total estimated time is 147 minutes"
    ]

    # Night hours tests
    response = client.get("/api/v1/find-route-by-time?origin=CC20&destination=NS21&time=2021-03-30T04:00")
    assert response.status_code == 200
    assert response.json() == [
        "Take CC from CC20 Farrer Road to CC17 Caldecott",
        "Change CC to TE",
        "Take TE from TE9 Caldecott to TE14 Orchard",
        "Change TE to NS",
        "Take NS from NS22 Orchard to NS21 Newton",
        "Done! Reach NS21 Newton. The total estimated time is 90 minutes"
    ]

    response = client.get("/api/v1/find-route-by-time?origin=CC20&destination=NS21&time=2021-03-30T12:00")
    assert response.status_code == 200
    assert response.json() == [
        "Take CC from CC20 Farrer Road to CC19 Botanic Gardens",
        "Change CC to DT",
        "Take DT from DT9 Botanic Gardens to DT11 Newton",
        "Change DT to NS",
        "Done! Reach NS21 Newton. The total estimated time is 46 minutes"
    ]

    # Non peak hours tests
    response = client.get("/api/v1/find-route-by-time?origin=NS1&destination=NS15&time=2021-03-30T12:00")
    assert response.status_code == 200
    assert response.json() == [
        "Take NS from NS1 Jurong East to NS15 Yio Chu Kang",
        "Done! Reach NS15 Yio Chu Kang. The total estimated time is 130 minutes"
    ]

    response = client.get("/api/v1/find-route-by-time?origin=NS1&destination=NS16&time=2021-03-30T12:00")
    assert response.status_code == 200
    assert response.json() == [
        "Take NS from NS1 Jurong East to NS1 Jurong East",
        "Change NS to EW",
        "Take EW from EW24 Jurong East to EW21 Buona Vista",
        "Change EW to CC",
        "Take CC from CC22 Buona Vista to CC15 Bishan",
        "Change CC to NS",
        "Take NS from NS17 Bishan to NS16 Ang Mo Kio",
        "Done! Reach NS16 Ang Mo Kio. The total estimated time is 130 minutes"
    ]

def test_find_route_by_time_with_error():
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

    response = client.get("/api/v1/find-route-by-time?origin=DT1&destination=DT2&time=2021-03-30T04:00")
    assert response.status_code == 400
    assert response.json() == [
        "Error: Line DT does not operate during night hours"
    ]
