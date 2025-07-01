from typing import List, Tuple

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.crud.crud import get_circuit_summary, get_driver_summary
from app.schemas.schemas import CircuitSummary, DriverSummary

# Create an APIRouter instance
router = APIRouter()


@router.get("/circuits/summary", response_model=List[CircuitSummary])
async def circuits_summary(
    db: AsyncSession = Depends(get_db_session),
) -> List[CircuitSummary]:
    """
    Retrieve a summary of circuits, including fastest lap time and total number
     of races.

    Args:
        db (AsyncSession): The database session dependency injected by FastAPI.

    Returns:
        List[CircuitSummary]: A list of CircuitSummary Pydantic models.
    """
    data: List[Tuple] = await get_circuit_summary(db)

    # Unpack the result tuples into CircuitSummary Pydantic model
    results = [
        CircuitSummary(
            **circuit.__dict__,  # Unpack Circuit model fields
            fastest_lap_ms=fastest_lap_ms,
            total_races=total_races,
        )
        for circuit, fastest_lap_ms, total_races in data
    ]
    return results


@router.get("/drivers/summary", response_model=List[DriverSummary])
async def drivers_summary(
    db: AsyncSession = Depends(get_db_session),
) -> List[DriverSummary]:
    """
    Retrieve a summary of drivers, including the number of podiums and total
    number of races.

    Args:
        db (AsyncSession): The database session dependency injected by FastAPI.

    Returns:
        List[DriverSummary]: A list of DriverSummary Pydantic models.
    """
    data: List[Tuple] = await get_driver_summary(db)

    # Unpack the result tuples into DriverSummary Pydantic model
    results = [
        DriverSummary(
            **driver.__dict__,  # Unpack Driver model fields
            podiums=podiums,
            total_races=total_races,
        )
        for driver, podiums, total_races in data
    ]
    return results
