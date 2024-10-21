"""
This module provides functions for interacting with the weather data stored in the database.

Functions:
1. `cleanup_old_realtime_weather()`: Removes records older than 24 hours from the `realtime_weather` table.
2. `insert_realtime_weather(dt, main_condition, temp, feels_like, pressure, humidity, rain, clouds, city)`: Inserts a new real-time weather record into the `realtime_weather` table.
3. `insert_daily_weather(date, avg_temp, max_temp, min_temp, dom_condition)`: Inserts a new daily weather record into the `daily_weather` table.
4. `insert_alert_event(dt, city, trigger, reason)`: Inserts a new alert event into the `alert_events` table.
5. `aggregate_daily_weather()`: Aggregates real-time weather data to daily summaries and inserts them into the `daily_weather` table.
6. `get_alerts()`: Retrieves all alert events from the `alert_events` table.
7. `get_historical_data()`: Retrieves all historical weather data from the `daily_weather` table and returns it as a JSON string.
8. `get_realtime_data()`: Retrieves all real-time weather data from the `realtime_weather` table and returns it as a JSON string.
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import datetime
import json

from weather_service.db_models import engine, RealtimeWeather, DailyWeather, AlertEvent

# Create a configured "Session" class
Session = sessionmaker(bind=engine)
session = Session()

def cleanup_old_realtime_weather():
    """
    Remove records from the `realtime_weather` table that are older than 24 hours.
    """
    cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=24)
    session.query(RealtimeWeather).filter(RealtimeWeather.dt < cutoff_time).delete(synchronize_session=False)
    session.commit()

async def insert_realtime_weather(dt, main_condition, temp, feels_like, pressure, humidity, rain, clouds, city):
    """
    Insert a new real-time weather record into the `realtime_weather` table and clean up old records.

    Parameters:
    - dt (datetime): Date and time of the weather report.
    - main_condition (str): Main weather condition description.
    - temp (float): Temperature in degrees.
    - feels_like (float): Perceived temperature.
    - pressure (float): Atmospheric pressure.
    - humidity (float): Humidity percentage.
    - rain (float): Rainfall amount.
    - clouds (float): Cloudiness percentage.
    - city (str): City name.
    """
    # Clean up old records
    cleanup_old_realtime_weather()
    
    new_data = RealtimeWeather(
        dt=dt,
        main_condition=main_condition,
        temp=temp,
        feels_like=feels_like,
        pressure=pressure,
        humidity=humidity,
        rain=rain,
        clouds=clouds,
        city=city
    )
    session.add(new_data)
    session.commit()

def insert_daily_weather(date, avg_temp, max_temp, min_temp, dom_condition):
    """
    Insert a new daily weather record into the `daily_weather` table.

    Parameters:
    - date (datetime.date): The date of the weather report.
    - avg_temp (float): Average temperature for the day.
    - max_temp (float): Maximum temperature for the day.
    - min_temp (float): Minimum temperature for the day.
    - dom_condition (str): Dominant weather condition for the day.
    """
    new_data = DailyWeather(
        date=date,
        avg_temp=avg_temp,
        max_temp=max_temp,
        min_temp=min_temp,
        dom_condition=dom_condition
    )
    session.add(new_data)
    session.commit()

def insert_alert_event(dt, city, trigger, reason):
    """
    Insert a new alert event into the `alert_events` table.

    Parameters:
    - dt (datetime): Date and time of the alert.
    - city (str): City name where the alert was issued.
    - trigger (str): The condition that triggered the alert.
    - reason (str): Reason for the alert.
    """
    new_event = AlertEvent(
        dt=dt,
        city=city,
        reason=reason,
        trigger=trigger,
    )
    session.add(new_event)
    session.commit()

def aggregate_daily_weather():
    """
    Aggregate real-time weather data to daily summaries and insert them into the `daily_weather` table.
    """
    today = datetime.date.today()
    start_time = datetime.datetime.combine(today, datetime.time.min)
    end_time = datetime.datetime.combine(today, datetime.time.max)
    
    result = session.query(
        RealtimeWeather.city,
        func.date(RealtimeWeather.dt).label('date'),
        func.avg(RealtimeWeather.temp).label('avg_temp'),
        func.max(RealtimeWeather.temp).label('max_temp'),
        func.min(RealtimeWeather.temp).label('min_temp'),
        func.max(RealtimeWeather.main_condition).label('dom_condition')
    ).filter(
        RealtimeWeather.dt >= start_time,
        RealtimeWeather.dt <= end_time
    ).group_by(
        RealtimeWeather.city,
        func.date(RealtimeWeather.dt)
    ).all()

    for row in result:
        daily_weather = DailyWeather(
            date=row.date,
            city=row.city,
            avg_temp=row.avg_temp,
            max_temp=row.max_temp,
            min_temp=row.min_temp,
            dom_condition=row.dom_condition
        )
        session.merge(daily_weather)
    
    session.commit()

def get_alerts():
    """
    Retrieve all alert events from the `alert_events` table.

    Returns:
    list: List of alert events.
    """
    alerts = session.query(AlertEvent).all()
    return alerts

def get_historical_data():
    """
    Retrieve all historical weather data from the `daily_weather` table and return it as a JSON string.

    Returns:
    str: JSON string containing historical weather data.
    """
    historical_data = session.query(DailyWeather).all()
    return json.dumps([data.__dict__ for data in historical_data])

def get_realtime_data():
    """
    Retrieve all real-time weather data from the `realtime_weather` table and return it as a JSON string.

    Returns:
    str: JSON string containing real-time weather data.
    """
    realtime_data = session.query(RealtimeWeather).all()
    data_list = [row.__dict__ for row in realtime_data]
        
    # Remove the SQLAlchemy internal properties
    for item in data_list:
        item.pop('_sa_instance_state', None)
    
    # Convert to JSON
    json_data = json.dumps(data_list, default=str)  # Use default=str to handle non-serializable fields like datetime
    
    return json_data
