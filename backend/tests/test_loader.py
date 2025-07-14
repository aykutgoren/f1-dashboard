from datetime import datetime

import pytest
import pandas as pd

from app.services.loader import (_parse_date_column, _parse_time_column, load_csv,
    load_circuits,
    load_drivers,
    load_races,
    load_driver_standings,
    load_lap_times,
    load_csv_to_db)


@pytest.mark.unit
def test_parse_date_column():
    # Create test DataFrame
    df = pd.DataFrame({"date_col": ["2021-01-01", "InvalidDate", "2022-05-06"]})

    # Expected behavior: InvalidDate should be converted to NaT (Not a Time)
    parsed_dates = _parse_date_column(df, "date_col")
    assert parsed_dates[0] == datetime(2021, 1, 1).date()
    assert pd.isna(parsed_dates[1])  # Invalid date should be NaT
    assert parsed_dates[2] == datetime(2022, 5, 6).date()


@pytest.mark.unit
def test_parse_time_column():
    # Create test DataFrame
    df = pd.DataFrame({"time_col": ["12:30:00", "InvalidTime", "15:45:30"]})

    # Expected behavior: InvalidTime should be converted to NaT (Not a Time)
    parsed_times = _parse_time_column(df, "time_col")
    assert parsed_times[0] == datetime.strptime("12:30:00", "%H:%M:%S").time()
    assert pd.isna(parsed_times[1])  # Invalid time should be NaT
    assert parsed_times[2] == datetime.strptime("15:45:30", "%H:%M:%S").time()

import pytest
import pandas as pd
from unittest.mock import AsyncMock, MagicMock, patch



# Sample CSV contents for testing specific loaders
CIRCUITS_CSV = """circuitId,circuitRef,name,location,country,lat,lng,alt,url
1,"albert_park","Albert Park Grand Prix Circuit","Melbourne","Australia",-37.8497,144.968,10,"http://en.wikipedia.org/wiki/Melbourne_Grand_Prix_Circuit"
"""

DRIVERS_CSV = """driverId,driverRef,number,code,forename,surname,dob,nationality,url
1,"hamilton",44,"HAM","Lewis","Hamilton","1985-01-07","British","http://en.wikipedia.org/wiki/Lewis_Hamilton"
"""

RACES_CSV = """raceId,year,round,circuitId,name,date,time,url,fp1_date,fp1_time,fp2_date,fp2_time,fp3_date,fp3_time,quali_date,quali_time,sprint_date,sprint_time
1,2009,1,1,"Australian Grand Prix","2009-03-29","06:00:00","http://en.wikipedia.org/wiki/2009_Australian_Grand_Prix",\\N,\\N,\\N,\\N,\\N,\\N,\\N,\\N,\\N,\\N
"""

DRIVER_STANDINGS_CSV = """driverStandingsId,raceId,driverId,points,position,positionText,wins
1,18,1,10,1,"1",1
"""

LAP_TIMES_CSV = """raceId,driverId,lap,position,time,milliseconds
841,20,1,1,"1:38.109",98109
"""

# Helper to write CSV content to tmp_path and return path
def write_csv(tmp_path, content, filename="test.csv"):
    file = tmp_path / filename
    file.write_text(content)
    return str(file)

@pytest.mark.unit
@pytest.mark.parametrize(
    "loader_func,csv_content",
    [
        (load_circuits, CIRCUITS_CSV),
        (load_drivers, DRIVERS_CSV),
        (load_races, RACES_CSV),
        (load_driver_standings, DRIVER_STANDINGS_CSV),
        (load_lap_times, LAP_TIMES_CSV),
    ],
)
def test_specific_loaders(tmp_path, loader_func, csv_content):
    csv_file = write_csv(tmp_path, csv_content)
    df = loader_func(csv_file)
    assert not df.empty
    # Check some expected columns exist for each loader
    expected_cols = df.columns.tolist()
    assert all(col in expected_cols for col in df.columns)

@pytest.mark.asyncio
@pytest.mark.unit
@patch("app.services.loader.load_circuits")
@patch("app.services.loader.load_drivers")
@patch("app.services.loader.load_races")
@patch("app.services.loader.load_driver_standings")
@patch("app.services.loader.load_lap_times")
async def test_load_csv_to_db(
    mock_load_lap_times,
    mock_load_driver_standings,
    mock_load_races,
    mock_load_drivers,
    mock_load_circuits,
):
    # Prepare dummy DataFrames returned by mocked loaders
    dummy_circuits = pd.DataFrame(
        [{"circuitId": 1, "circuitRef": "ref1", "name": "c1", "location": "loc", "country": "country", "lat": 1.1, "lng": 2.2, "alt": None, "url": "url"}]
    )
    dummy_drivers = pd.DataFrame(
        [{"driverId": 1, "driverRef": "ref2", "number": 44, "code": "H", "forename": "F", "surname": "S", "dob": pd.Timestamp("2025-01-01"), "nationality": "nat", "url": "url"}]
    )
    dummy_races = pd.DataFrame(
        [{"raceId": 1, "year": 2025, "round": 1, "circuitId": 1, "name": "race1", "date": pd.Timestamp("2025-01-01"), "time": None, "url": "url"}]
    )
    dummy_driver_standings = pd.DataFrame(
        [{"driverStandingsId": 1, "raceId": 1, "driverId": 1, "points": 25.0, "position": 1.0, "positionText": "1", "wins": 1}]
    )
    dummy_lap_times = pd.DataFrame(
        [{"raceId": 1, "driverId": 1, "lap": 1, "position": 1, "time": "1:30.123", "milliseconds": 90123.0}]
    )

    mock_load_circuits.return_value = dummy_circuits
    mock_load_drivers.return_value = dummy_drivers
    mock_load_races.return_value = dummy_races
    mock_load_driver_standings.return_value = dummy_driver_standings
    mock_load_lap_times.return_value = dummy_lap_times

    # Mock AsyncSession with add_all and commit tracking
    mock_session = AsyncMock()
    mock_session.add_all = MagicMock()
    mock_session.commit = AsyncMock()

    await load_csv_to_db(mock_session)

    # Verify add_all called multiple times (for each entity type)
    assert mock_session.add_all.call_count == 5

    # Verify commit called once
    mock_session.commit.assert_awaited_once()