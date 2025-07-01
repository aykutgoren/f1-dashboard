from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta

# Create a base class for all models to inherit from
# `Base` will be used as the base class for SQLAlchemy ORM models
Base: DeclarativeMeta = declarative_base()
