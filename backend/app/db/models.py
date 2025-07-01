from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Time
from sqlalchemy.orm import relationship

from app.db.base import Base


class Circuit(Base):
    __tablename__ = "circuits"

    circuit_id = Column(Integer, primary_key=True, index=True)
    circuit_ref = Column(String)
    name = Column(String)
    location = Column(String)
    country = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    alt = Column(Integer, nullable=True)
    url = Column(String)

    # Establish the relationship with the 'Race' model
    races = relationship("Race", back_populates="circuit")


class Driver(Base):
    __tablename__ = "drivers"

    driver_id = Column(Integer, primary_key=True, index=True)
    driver_ref = Column(String)
    number = Column(Integer, nullable=True)
    code = Column(String, nullable=True)
    forename = Column(String)
    surname = Column(String)
    dob = Column(Date)
    nationality = Column(String)
    url = Column(String)

    # Establish relationships with other models
    standings = relationship("DriverStanding", back_populates="driver")
    lap_times = relationship("LapTime", back_populates="driver")


class Race(Base):
    __tablename__ = "races"

    race_id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    round = Column(Integer)
    circuit_id = Column(Integer, ForeignKey("circuits.circuit_id"))
    name = Column(String)
    date = Column(Date)
    time = Column(Time, nullable=True)
    url = Column(String)
    fp1_date = Column(Date, nullable=True)
    fp1_time = Column(Time, nullable=True)
    fp2_date = Column(Date, nullable=True)
    fp2_time = Column(Time, nullable=True)
    fp3_date = Column(Date, nullable=True)
    fp3_time = Column(Time, nullable=True)
    quali_date = Column(Date, nullable=True)
    quali_time = Column(Time, nullable=True)
    sprint_date = Column(Date, nullable=True)
    sprint_time = Column(Time, nullable=True)

    # Establish relationships with other models
    circuit = relationship("Circuit", back_populates="races")
    standings = relationship("DriverStanding", back_populates="race")
    lap_times = relationship("LapTime", back_populates="race")


class DriverStanding(Base):
    __tablename__ = "driver_standings"

    driver_standings_id = Column(Integer, primary_key=True, index=True)
    race_id = Column(Integer, ForeignKey("races.race_id"))
    driver_id = Column(Integer, ForeignKey("drivers.driver_id"))
    points = Column(Float)
    position = Column(Integer)
    position_text = Column(String)
    wins = Column(Integer)

    # Establish relationships with other models
    driver = relationship("Driver", back_populates="standings")
    race = relationship("Race", back_populates="standings")


class LapTime(Base):
    __tablename__ = "lap_times"

    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(Integer, ForeignKey("races.race_id"))
    driver_id = Column(Integer, ForeignKey("drivers.driver_id"))
    lap = Column(Integer)
    position = Column(Integer)
    time = Column(String)
    milliseconds = Column(Integer)

    # Establish relationships with other models
    driver = relationship("Driver", back_populates="lap_times")
    race = relationship("Race", back_populates="lap_times")
