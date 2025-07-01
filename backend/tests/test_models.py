from datetime import date, time

import pytest

from app.db.models import Circuit, Driver, Race, DriverStanding, LapTime


@pytest.mark.unit
def test_circuit_model_fields() -> None:
    """
    Test the Circuit model fields.

    Ensures that the Circuit model attributes are correctly set.
    """
    circuit = Circuit(
        circuit_id=1,
        circuit_ref="albert_park",
        name="Albert Park",
        location="Melbourne",
        country="Australia",
        lat=-37.8497,
        lng=144.968,
        alt=10,
        url="http://example.com",
    )
    assert circuit.name == "Albert Park"
    assert circuit.circuit_id == 1


@pytest.mark.unit
def test_driver_model_fields() -> None:
    """
    Test the Driver model fields.

    Ensures that the Driver model attributes are correctly set.
    """
    driver = Driver(
        driver_id=44,
        driver_ref="hamilton",
        number=44,
        code="HAM",
        forename="Lewis",
        surname="Hamilton",
        dob="1985-01-07",
        nationality="British",
        url="http://example.com",
    )
    assert driver.surname == "Hamilton"
    assert driver.driver_id == 44


@pytest.mark.unit
def test_race_model_fields() -> None:
    """
    Test the Race model fields.

    Ensures that the Race model attributes are correctly set.
    """
    race = Race(
        race_id=1,
        year=2023,
        round=5,
        circuit_id=10,
        name="Monaco Grand Prix",
        date=date(2023, 5, 28),
        time=time(14, 0),
        url="http://example.com/race",
        fp1_date=date(2023, 5, 26),
        fp1_time=time(10, 0),
        fp2_date=date(2023, 5, 27),
        fp2_time=time(10, 0),
        fp3_date=None,
        fp3_time=None,
        quali_date=date(2023, 5, 27),
        quali_time=time(14, 0),
        sprint_date=None,
        sprint_time=None,
    )
    assert race.name == "Monaco Grand Prix"
    assert race.year == 2023
    assert race.circuit_id == 10
    assert race.fp1_date == date(2023, 5, 26)
    assert race.fp3_date is None


@pytest.mark.unit
def test_driver_standing_model_fields() -> None:
    """
    Test the DriverStanding model fields.

    Ensures that the DriverStanding model attributes are correctly set.
    """
    standing = DriverStanding(
        driver_standings_id=1,
        race_id=1,
        driver_id=44,
        points=25.0,
        position=1,
        position_text="1",
        wins=5,
    )
    assert standing.position == 1
    assert standing.points == 25.0
    assert standing.wins == 5


@pytest.mark.unit
def test_lap_time_model_fields() -> None:
    """
    Test the LapTime model fields.

    Ensures that the LapTime model attributes are correctly set.
    """
    lap_time = LapTime(
        id=1,
        race_id=1,
        driver_id=44,
        lap=15,
        position=1,
        time="1:15.234",
        milliseconds=75234,
    )
    assert lap_time.lap == 15
    assert lap_time.position == 1
    assert lap_time.time == "1:15.234"
    assert lap_time.milliseconds == 75234
