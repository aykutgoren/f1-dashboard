from typing import List, Tuple

from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Circuit, Driver, Race, DriverStanding, LapTime


async def get_circuit_summary(db: AsyncSession) -> List[Tuple[Circuit, int, int]]:
    """
    Retrieve a summary of circuits, including the fastest lap in milliseconds
    and the total number of races.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[Tuple[Circuit, int, int]]: A list of tuples with Circuit, fastest
        lap (in ms), and total races.
    """
    # Subquery to get the fastest lap time for each race
    sub_fastest_lap = (
        select(LapTime.race_id, func.min(LapTime.milliseconds).label("fastest_lap_ms"))
        .group_by(LapTime.race_id)
        .subquery()
    )

    # Main query to get circuit details, fastest lap time, and total races
    query = (
        select(
            Circuit,
            func.min(sub_fastest_lap.c.fastest_lap_ms).label("fastest_lap_ms"),
            func.count(Race.race_id).label("total_races"),
        )
        .join(Race, Circuit.circuit_id == Race.circuit_id)
        .join(sub_fastest_lap, Race.race_id == sub_fastest_lap.c.race_id)
        .group_by(Circuit.circuit_id)
    )

    # Execute the query and return the result
    result = await db.execute(query)
    return result.all()


async def get_driver_summary(db: AsyncSession) -> List[Tuple[Driver, int, int]]:
    """
    Retrieve a summary of drivers, including the number of podiums and total
    races entered.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[Tuple[Driver, int, int]]: A list of tuples with Driver, podium
        count, and total races.
    """
    # Subquery to count podiums (positions 1-3) for each driver
    podium_subq = (
        select(DriverStanding.driver_id, func.count().label("podiums"))
        .where(DriverStanding.position.in_([1, 2, 3]))
        .group_by(DriverStanding.driver_id)
        .subquery()
    )

    # Subquery to count total races entered for each driver
    races_subq = (
        select(DriverStanding.driver_id, func.count().label("total_races"))
        .group_by(DriverStanding.driver_id)
        .subquery()
    )

    # Main query to get driver details, podiums, and total races
    query = (
        select(
            Driver,
            func.coalesce(
                podium_subq.c.podiums, 0
            ),  # Use coalesce to default podiums to 0 if none found
            func.coalesce(
                races_subq.c.total_races, 0
            ),  # Use coalesce to default total races to 0 if none found
        )
        .outerjoin(podium_subq, Driver.driver_id == podium_subq.c.driver_id)
        .outerjoin(races_subq, Driver.driver_id == races_subq.c.driver_id)
    )

    # Execute the query and return the result
    result = await db.execute(query)
    return result.all()
