from typing import Optional

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Circuit, Driver, DriverStanding, LapTime, Race

# NA_VALUES for missing data handling in CSVs
NA_VALUES = ["\\N", "NaN", "None", ""]


# Helper function to parse date columns
def _parse_date_column(df: pd.DataFrame, col: str) -> pd.Series:
    """Convert a column to datetime.date, returning None for invalid entries."""
    return pd.to_datetime(df[col], format="%Y-%m-%d", errors="coerce").dt.date


# Helper function to parse time columns
def _parse_time_column(df: pd.DataFrame, col: str) -> pd.Series:
    """Convert a column to datetime.time."""
    return pd.to_datetime(df[col], format="%H:%M:%S", errors="coerce").dt.time


# General function to load CSVs with specific parsing
def load_csv(
    path: str,
    dtype: dict,
    date_columns: Optional[list] = None,
    time_columns: Optional[list] = None,
) -> pd.DataFrame:
    """Generic CSV loader that also handles date/time columns."""
    df = pd.read_csv(path, dtype=dtype, na_values=NA_VALUES, keep_default_na=True)
    if date_columns:
        for col in date_columns:
            df[col] = _parse_date_column(df, col)
    if time_columns:
        for col in time_columns:
            df[col] = _parse_time_column(df, col)
    df = df.where(
        pd.notnull(df), None
    )  # Replace NaNs with None for SQLAlchemy compatibility
    return df


# Load Circuits
def load_circuits(path: str = "dataset/circuits.csv") -> pd.DataFrame:
    dtype = {
        "circuit_id": "int64",
        "circuit_ref": "string",
        "name": "string",
        "location": "string",
        "country": "string",
        "lat": "float64",
        "lng": "float64",
        "alt": "float64",  # nullable
        "url": "string",
    }
    return load_csv(path, dtype)


# Load Drivers
def load_drivers(path: str = "dataset/drivers.csv") -> pd.DataFrame:
    dtype = {
        "driver_id": "int64",
        "driver_ref": "string",
        "number": "float64",
        "code": "string",
        "forename": "string",
        "surname": "string",
        "nationality": "string",
        "url": "string",
    }
    return load_csv(path, dtype, date_columns=["dob"])


# Load Races
def load_races(path: str = "dataset/races.csv") -> pd.DataFrame:
    dtype = {
        "race_id": "int64",
        "year": "int64",
        "round": "int64",
        "circuit_id": "int64",
        "name": "string",
        "url": "string",
    }
    return load_csv(
        path,
        dtype,
        date_columns=[
            "date",
            "fp1_date",
            "fp2_date",
            "fp3_date",
            "quali_date",
            "sprint_date",
        ],
        time_columns=[
            "time",
            "fp1_time",
            "fp2_time",
            "fp3_time",
            "quali_time",
            "sprint_time",
        ],
    )


# Load Driver Standings
def load_driver_standings(path: str = "dataset/driver_standings.csv") -> pd.DataFrame:
    dtype = {
        "driver_standings_id": "int64",
        "race_id": "int64",
        "driver_id": "int64",
        "points": "float64",
        "position": "float64",  # nullable
        "position_text": "string",
        "wins": "int64",
    }
    return load_csv(path, dtype)


# Load Lap Times
def load_lap_times(path: str = "dataset/lap_times.csv") -> pd.DataFrame:
    dtype = {
        "race_id": "int64",
        "driver_id": "int64",
        "lap": "int64",
        "position": "int64",
        "time": "string",
        "milliseconds": "float64",
    }
    return load_csv(path, dtype)


# Function to insert all the data into the database (using bulk insert for efficiency)
async def load_csv_to_db(session: AsyncSession):
    # Load CSVs
    circuits_df = load_circuits()
    drivers_df = load_drivers()
    races_df = load_races()
    driver_standings_df = load_driver_standings()
    lap_times_df = load_lap_times()

    # Bulk insert Circuits
    circuits = [
        Circuit(
            circuit_id=row["circuitId"],
            circuit_ref=row["circuitRef"],
            name=row["name"],
            location=row["location"],
            country=row["country"],
            lat=row["lat"],
            lng=row["lng"],
            alt=row.get("alt", None),
            url=row["url"],
        )
        for _, row in circuits_df.iterrows()
    ]
    session.add_all(circuits)

    # Bulk insert Drivers
    drivers = [
        Driver(
            driver_id=row["driverId"],
            driver_ref=row["driverRef"],
            number=row["number"] if not pd.isna(row["number"]) else None,
            code=row["code"] if not pd.isna(row["code"]) else None,
            forename=row["forename"],
            surname=row["surname"],
            dob=row["dob"],
            nationality=row["nationality"],
            url=row["url"],
        )
        for _, row in drivers_df.iterrows()
    ]
    session.add_all(drivers)

    # Bulk insert Driver Standings
    driver_standings = [
        DriverStanding(
            driver_standings_id=row["driverStandingsId"],
            race_id=row["raceId"],
            driver_id=row["driverId"],
            points=row["points"],
            position=row["position"],
            position_text=row["positionText"],
            wins=row["wins"],
        )
        for _, row in driver_standings_df.iterrows()
    ]
    session.add_all(driver_standings)

    # Bulk insert Lap Times
    lap_times = [
        LapTime(
            race_id=row["raceId"],
            driver_id=row["driverId"],
            lap=row["lap"],
            position=row["position"],
            time=row["time"],
            milliseconds=row["milliseconds"],
        )
        for _, row in lap_times_df.iterrows()
    ]
    session.add_all(lap_times)

    # Bulk insert Races
    races = [
        Race(
            race_id=row["raceId"],
            year=row["year"],
            round=row["round"],
            circuit_id=row["circuitId"],
            name=row["name"],
            date=row["date"],
            time=row["time"],
            url=row["url"],
        )
        for _, row in races_df.iterrows()
    ]
    session.add_all(races)

    # Commit all the changes to the database
    await session.commit()
