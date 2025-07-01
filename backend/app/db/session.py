from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create an asynchronous SQLAlchemy engine for the database connection
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Define the session maker for async sessions
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Asynchronous context manager to get the database session
async def get_db_session() -> AsyncSession:
    """
    Get a database session for async database operations.

    Returns:
        AsyncSession: The database session for interacting with the DB.
    """
    async with AsyncSessionLocal() as session:
        yield session  # Return the session object for use in API endpoints
