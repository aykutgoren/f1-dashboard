import logging

from app.db.models import Base


# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Function to create tables
async def create_tables(engine):
    try:
        # Start a synchronous connection to run DDL operations
        async with engine.begin() as conn:  # Start a transaction
            # Run the create_all method to create all tables in the metadata
            await conn.run_sync(Base.metadata.create_all)

        # Log success
        logger.info("Tables created (or verified as existing).")
    except Exception as e:
        # Log any errors
        logger.error(f"Error creating tables: {e}")
