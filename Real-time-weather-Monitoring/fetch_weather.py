import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
api_key = os.getenv('OPENWEATHER_API_KEY')

def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# List of cities to fetch weather data for
cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

# Fetch and print weather data for each city
for city in cities:
    data = get_weather_data(city, api_key)
    if data:
        print(f"City: {city}, Temperature: {data['main']['temp']}°C, Weather: {data['weather'][0]['description']}")
    else:
        print(f"Failed to retrieve data for {city}")
