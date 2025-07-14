from datetime import date

import pytest


from app.db.models import Circuit, Driver, Race, DriverStanding, LapTime
from app.crud.crud import get_circuit_summary, get_driver_summary


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_circuit_summary(async_session):
    # Prepare test data
    circuit = Circuit(
        circuit_id=1, name="Test Circuit", location="Test City", country="Testland"
    )
    race = Race(
        race_id=1,
        circuit_id=1,
        year=2025,
        round=1,
        name="Test GP",
        date=date(2025, 1, 1),
    )
    lap1 = LapTime(race_id=1, driver_id=1, lap=1, position=1, milliseconds=88001)
    lap2 = LapTime(race_id=1, driver_id=2, lap=1, position=2, milliseconds=88000)

    async_session.add_all([circuit, race, lap1, lap2])
    await async_session.commit()

    # Test function
    results = await get_circuit_summary(async_session)

    assert len(results) == 1
    circuit_result, fastest_lap_ms, total_races = results[0]
    assert circuit_result.name == "Test Circuit"
    assert fastest_lap_ms == 88000
    assert total_races == 1


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_driver_summary(async_session):
    # Prepare test data
    driver1 = Driver(driver_id=1, forename="test_forname_1", surname="test_surname_1")
    driver2 = Driver(driver_id=2, forename="test_forname_2", surname="test_surname_2")

    ds1 = DriverStanding(race_id=1, driver_id=1, points=25.0, position=1)
    ds2 = DriverStanding(race_id=1, driver_id=2, points=18.0, position=2)
    ds3 = DriverStanding(race_id=2, driver_id=1, points=15.0, position=4)

    race2 = Race(
        race_id=2,
        circuit_id=1,
        year=2024,
        round=2,
        name="Second GP",
        date=date(2024, 1, 8),
    )

    async_session.add_all([driver1, driver2, ds1, ds2, ds3, race2])
    await async_session.commit()

    # Test function
    results = await get_driver_summary(async_session)

    driver_summaries = {
        driver.driver_id: (driver, podiums, total_races)
        for driver, podiums, total_races in results
    }

    assert driver_summaries[1][1] == 1  # test_forname_1 test_surname_1 has 1 podium
    assert driver_summaries[1][2] == 2  # test_forname_1 test_surname_1 raced 2 times
    assert driver_summaries[2][1] == 1  # test_forname_2 test_surname_2 has 1 podium
    assert driver_summaries[2][2] == 1  # test_forname_2 test_surname_2 Smith raced once
