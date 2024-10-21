"""
This module sets up the database schema for storing weather-related data using SQLAlchemy ORM.

It defines three primary tables:
1. `realtime_weather`: Stores real-time weather data.
2. `daily_weather`: Stores daily aggregated weather data.
3. `alert_events`: Stores alert events related to weather conditions.

The module initializes the SQLAlchemy engine using credentials fetched from environment variables.
"""

import os
from sqlalchemy import create_engine, Column, String, Date, Numeric, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Fetching database connection details from environment variables
DB_USER = os.getenv('DB_USER', 'default_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'default_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'mydatabase')

# Initialize the base class for declarative class definitions
Base = declarative_base()

class RealtimeWeather(Base):
    """
    Represents real-time weather data in the 'realtime_weather' table.
    
    Columns:
    - dt (TIMESTAMP): Date and time of the weather report.
    - main_condition (String): Main weather condition description.
    - temp (Numeric): Temperature in degrees.
    - feels_like (Numeric): Perceived temperature.
    - pressure (Numeric): Atmospheric pressure.
    - humidity (Numeric): Humidity percentage.
    - rain (Numeric): Rainfall amount.
    - clouds (Numeric): Cloudiness percentage.
    - city (String): City name.
    """
    __tablename__ = 'realtime_weather'
    
    dt = Column(TIMESTAMP, nullable=False, primary_key=True)
    main_condition = Column(String, nullable=False)
    temp = Column(Numeric, nullable=False)
    feels_like = Column(Numeric, nullable=False)
    pressure = Column(Numeric, nullable=False)
    humidity = Column(Numeric, nullable=False)
    rain = Column(Numeric, nullable=False)
    clouds = Column(Numeric, nullable=False)
    city = Column(String, nullable=False, primary_key=True)


class DailyWeather(Base):
    """
    Represents daily aggregated weather data in the 'daily_weather' table.
    
    Columns:
    - date (Date): The date of the weather report.
    - city (String): City name.
    - avg_temp (Numeric): Average temperature for the day.
    - max_temp (Numeric): Maximum temperature for the day.
    - min_temp (Numeric): Minimum temperature for the day.
    - dom_condition (String): Dominant weather condition for the day.
    """
    __tablename__ = 'daily_weather'
    
    date = Column(Date, primary_key=True)
    city = Column(String, primary_key=True)
    avg_temp = Column(Numeric, nullable=False)
    max_temp = Column(Numeric, nullable=False)
    min_temp = Column(Numeric, nullable=False)
    dom_condition = Column(String, nullable=False)


class AlertEvent(Base):
    """
    Represents weather alert events in the 'alert_events' table.
    
    Columns:
    - event_id (UUID): Unique identifier for the alert event.
    - dt (TIMESTAMP): Date and time of the alert.
    - city (String): City name where the alert was issued.
    - reason (String): Reason for the alert.
    - trigger (String): The condition that triggered the alert.
    """
    __tablename__ = 'alert_events'
    
    event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dt = Column(TIMESTAMP, nullable=False)
    city = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    trigger = Column(String, nullable=False)

# Create an engine and initialize the database schema
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URL)

# Create all tables defined in the Base metadata
Base.metadata.create_all(engine)
