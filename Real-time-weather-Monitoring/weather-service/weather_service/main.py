"""
API Contracts and Scheduler Setup

This module sets up the FastAPI application with integrated Dash apps and schedules periodic jobs 
for aggregating daily weather data and fetching real-time weather data. It also defines API endpoints 
for fetching alerts in JSON and HTML formats.

Dependencies:
- FastAPI
- APScheduler
- dotenv
- Logging
- Weather Service Modules (db_utils, utils, dash_app_statistics, dash_app_threshold, dash_app_alerts)

Configuration:
- Environment variables for API keys and database credentials.
- Scheduler for periodic tasks.
"""

import os
import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.wsgi import WSGIMiddleware
from dotenv import load_dotenv

from weather_service.db_utils import aggregate_daily_weather, get_alerts
from weather_service.utils import check_data_against_alerts, fetch_weather_data, insert_fetched_data, rate_limit, thresholds
from weather_service.dash_app_statistics import app as dash_app_statistics
from weather_service.dash_app_threshold import app as dash_app_threshold
from weather_service.dash_app_alerts import app as dash_app_alerts

# Load environment variables
load_dotenv()
logging.basicConfig(format='%(asctime)s %(user)-8s %(message)s')

# Scheduler setup
scheduler = AsyncIOScheduler()

# Constants
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
API_URL = 'https://api.openweathermap.org/data/2.5/weather'
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

def scheduled_job():
    """
    Job to aggregate daily weather data.
    """
    aggregate_daily_weather()

async def fetch_and_insert_data():
    """
    Fetch and insert real-time weather data for configured cities.
    """
    logging.info("Fetching and inserting data real-time.")
    for city in CITIES:
        try:
            weather_data = await fetch_weather_data(API_URL, OPENWEATHER_API_KEY, city)
            await insert_fetched_data(weather_data)
            await check_data_against_alerts(weather_data, thresholds.get_thresholds())
            logging.info(f"Data fetched and inserted for {city}")
        except Exception as e:
            logging.error(f"Failed to insert data for {city}: {e}")

# Scheduler jobs
scheduler.add_job(aggregate_daily_weather, 'cron', hour=0, minute=1)
scheduler.add_job(fetch_and_insert_data, IntervalTrigger(seconds=30))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for starting and stopping the scheduler.

    Parameters:
    app (FastAPI): The FastAPI application instance.
    """
    scheduler.start()
    yield
    scheduler.shutdown()

# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)

# Mount Dash apps
app.mount("/statistics", WSGIMiddleware(dash_app_statistics.server))
app.mount("/configs", WSGIMiddleware(dash_app_threshold.server))
app.mount("/alerts", WSGIMiddleware(dash_app_alerts.server))

# API Endpoints

@app.get("/")
@rate_limit(limit=5, interval=60)
async def hello(request: Request):
    """
    Health check endpoint.

    Parameters:
    request (Request): The incoming request object.

    Returns:
    dict: Status message.
    """
    return {"status": "ok"}

@app.get("/alerts/json")
@rate_limit(limit=5, interval=60)
async def get_alerts_json(request: Request):
    """
    Retrieve alerts in JSON format.

    Parameters:
    request (Request): The incoming request object.

    Returns:
    list: List of alert events in JSON format.
    """
    try:
        alerts = get_alerts()
        return alerts
    except Exception as e:
        raise HTTPException(status_code=401, detail=getattr(e, 'message', repr(e)))

@app.get("/alerts/html")
@rate_limit(limit=5, interval=60)
async def get_alerts_html(request: Request):
    """
    Retrieve alerts in HTML format.

    Parameters:
    request (Request): The incoming request object.

    Returns:
    HTMLResponse: HTML formatted alerts.
    """
    try:
        alerts = get_alerts()
        # Convert alerts to HTML table
        table_html = "<table>"
        table_html += "<tr><th>Alert ID</th><th>Timestamp</th><th>City</th><th>Reason</th><th>Trigger</th></tr>"
        for alert in alerts:
            table_html += f"<tr>\
            <td>{alert.event_id}</td>\
            <td>{alert.dt}</td>\
            <td>{alert.city}</td>\
            <td>{alert.reason}</td>\
            <td>{alert.trigger}</td></tr>"
        table_html += "</table>"
        return HTMLResponse(table_html)
    except Exception as e:
        raise HTTPException(status_code=401, detail=getattr(e, 'message', repr(e)))
