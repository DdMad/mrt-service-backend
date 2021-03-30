
# MRT Route Service Backend
This is a backend service that provides APIs to compute a route between 2 MRT stations that has least stops to travel or takes least time to travel.
## Get Started
### Requirement
Python 3.6+

### Run
First, clone the repo or get the repo from somewhere. And then:
```bash
pip install -r requirements.txt
```
Once `pip install` completes, run:
```bash
uvicorn app.main:app --reload
```
This will start the backend service app on `127.0.0.1:8000`.

Then you can either call the API by entering the API url with parameters in the browser.
For example, the API request below will get the route from NS1 to NS16 which has the least stops:
```bash
GET http://127.0.0.1:8000/api/v1/find-route-by-stop?origin=NS1&destination=NS16
```
Or you can open `127.0.0.1:8000/docs` to check the document about the API and play with the API there.

### Examples
1. Find the route between `EW23` and `CG1` that has least stops:
`GET http://127.0.0.1:8000/api/v1/find-route-by-stop?origin=EW23&destination=CG1`
The response should be:
`["Take EW from EW23 Clementi to EW4 Tanah Merah",
"Change EW to CG",
"Take CG from CG0 Tanah Merah to CG1 Expo",
"In total it takes 21 stops"]`

2. Find the route between `NS1` and `NS16` at `2020-03-30T08:00` that takes least time:
`GET http://127.0.0.1:8000/api/v1/find-route-by-time?origin=NS1&destination=NS16&time=2020-03-30T08:00`
The response should be:
`["Take NS from NS1 Jurong East to NS1 Jurong East","Change NS to EW","Take EW from EW24 Jurong East to EW21 Buona Vista","Change EW to CC","Take CC from CC22 Buona Vista to CC15 Bishan","Change CC to NS","Take NS from NS17 Bishan to NS16 Ang Mo Kio","The total estimated time is 147 minutes"]`

### Run Tests
Make sure you have done the `pip install` part in the previous **Run** session.
```bash
pytest
```
This will start running all the tests of this backend service app.

## Documentation
### APIs
| API | Description | Method | Parameters | Response |
| -- | -- | -- | -- | -- |
| `/api/v1/find-route-by-stop` | Find the route from **origin** to **destination** that has the least stops to travel | GET | **origin** (str): the start station (e.g. `EW23`) <br> **destination** (str): the end station  (e.g. `EW23`) | **List[str]**: human-readable steps to take |
| `/api/v1/find-route-by-time` | Find the route from **origin** to **destination** that takes the least time to travel at given **time** | GET | **origin** (str): the start station  (e.g. `EW23`) <br> **destination** (str): the end station  (e.g. `EW23`) <br> **time** (str): the start time in format `%Y-%m-%dT%H:%M` (more info about the [datetime format](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)) (e.g. `2020-03-30T08:00`) | **List[str]**: human-readable steps to take |

### Some Assumptions
#### For API `/api/v1/find-route-by-stop`:
 - It treats line changing as one stop as well. For example, from **EW23** to **CC21**, you need to change line from **EW** to **CC** at **EW21/CC22 Buona Vista**, and there will be one stop from **EW21** to **CC22** (the route returned from the API will be **EW23 -> EW22 -> EW21 -> CC22 -> CC21**, which in total 4 stops).
 - It will only return 1 route that has least stops. If multiple routes with the same number of stops exists, it will return 1 of them.
#### For API `/api/v1/find-route-by-time`:
- It will use the time that user passed to API to determine peak/night/non-peak hours for the whole trip. For example, if the time parameter is set to `2021-03-30T17:00`, which is in non-peak hours. Even if it takes 2 hours to finish the trip (i.e. some part of the trip will fall in peak hours), the whole trip will still be considered in non-peak hours.

### Future Improvements
1. **Return top n routes instead of 1 route only**
For API `/api/v1/find-route-by-stop`, this already can be done easily. However, for API `/api/v1/find-route-by-time`, it's a bit complicated (but it's still doable according to [Yen's algorithm](https://en.wikipedia.org/wiki/Yen%27s_algorithm)). So due to the time constraints and to make  these 2 APIs consistent, we just return 1 route only.

2. **Determine the peak/night/non-peak hours based on the current time dynamically instead of start time**
Currently, it will just use start time (i.e. the time parameter that is passed by user) to determine the peak/night/non-peak hours for the whole trip. However, to make it more accurate, it should use the current time to determine whether now is in peak/night/non-peak hours for each stop it travels .
