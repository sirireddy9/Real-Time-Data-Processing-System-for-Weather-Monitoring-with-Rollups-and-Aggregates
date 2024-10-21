import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('OPENWEATHER_API_KEY')

# Function to fetch weather data
def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to convert temperature based on user preference
def convert_temperature(temp_kelvin, unit):
    if unit == 'C':
        # Convert to Celsius
        return temp_kelvin - 273.15
    elif unit == 'F':
        # Convert to Fahrenheit
        return (temp_kelvin - 273.15) * 9/5 + 32
    else:
        return temp_kelvin  # Kelvin by default

# Get user preference for temperature unit
unit = input("Enter preferred temperature unit (C for Celsius, F for Fahrenheit): ").upper()

# List of cities to fetch weather data for
cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

# Fetch and print weather data for each city
for city in cities:
    data = get_weather_data(city, api_key)
    if data:
        temp_kelvin = data['main']['temp']
        temp_converted = convert_temperature(temp_kelvin, unit)
        weather_description = data['weather'][0]['description']
        
        # Print the result with the preferred unit
        if unit == 'C':
            print(f"City: {city}, Temperature: {temp_converted:.2f}°C, Weather: {weather_description}")
        elif unit == 'F':
            print(f"City: {city}, Temperature: {temp_converted:.2f}°F, Weather: {weather_description}")
        else:
            print(f"City: {city}, Temperature: {temp_converted:.2f}K, Weather: {weather_description}")
    else:
        print(f"Failed to retrieve data for {city}")
