import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to fetch weather data for a given city
def get_weather_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    print(f"Fetching weather data for {city}...")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch weather data for {city}. Error: {response.text}")
        return None

# Function to check if an alert is needed based on temperature
def check_alerts(city, temp):
    threshold = 35
    if temp > threshold:
        print(f"**ALERT**: {city} has exceeded the threshold temperature of {threshold}°C with {temp}°C!")
    else:
        print(f"No alerts for {city}. The current temperature is {temp}°C. Environment is clear.")

# Main function to fetch and check weather for multiple cities
def fetch_weather_alerts():
    # Load the OpenWeather API key from the environment variable
    api_key = os.getenv('OPENWEATHER_API_KEY')

    if not api_key:
        print("Error: No API key found! Please set the 'OPENWEATHER_API_KEY' environment variable.")
        return

    # List of cities to fetch weather for
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

    for city in cities:
        data = get_weather_data(city, api_key)
        if data:
            temp = data['main']['temp']
            check_alerts(city, temp)
        else:
            print(f"No weather data available for {city}.")

# Call the function to fetch and check weather for all cities
fetch_weather_alerts()
