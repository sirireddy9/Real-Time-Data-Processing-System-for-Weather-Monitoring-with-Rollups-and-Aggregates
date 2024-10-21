import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    print(f"Request URL: {url}")
    print(f"City: {city}, Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response Data: {response.json()}")
        return response.json()
    else:
        print(f"Error: {response.text}")
        return None

# Fetch weather data for multiple cities
api_key = os.getenv('OPENWEATHER_API_KEY')
cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

for city in cities:
    print(f"Fetching weather for {city}...")
    data = get_weather_data(city, api_key)
    if data:
        print(f"City: {city}, Temperature: {data['main']['temp']}°C")
    else:
        print(f"Failed to fetch weather data for {city}.")
