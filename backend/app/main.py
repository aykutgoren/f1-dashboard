from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import delete, inspect

from app.db.session import engine, get_db_session
from app.services.table_creator import create_tables
from app.db.models import LapTime, DriverStanding, Race, Driver, Circuit
from app.db.session import AsyncSessionLocal
from app.api import routes
from app.services.loader import load_csv_to_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Startup logic
    async with AsyncSessionLocal() as db:
        async with engine.begin() as conn:
            existing_tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        for model in [LapTime, DriverStanding, Race, Driver, Circuit]:
            # Delete tables if they exist
            if model.__tablename__ in existing_tables:
                await db.execute(delete(model))
        # Create tables (DDL) using engine if they don't exist
        await create_tables(engine)
        # Insert records (DML) using session
        await load_csv_to_db(db)

    yield  # Hand over to FastAPI to continue running the app

    # ❌ No shutdown logic needed, as nothing specific to handle on shutdown

app = FastAPI(lifespan=lifespan, title="F1 Data API")
app.include_router(routes.router, prefix="/api")

# Allow requests from Vite dev server (React)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Add middleware for CORS handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the root endpoint
@app.get("/")
async def root() -> dict:
    """
    Root endpoint to check if the F1 Dashboard Backend is running.

    Returns:
        dict: A message confirming the server is up and running.
    """
    return {"message": "F1 Dashboard Backend Running"}

