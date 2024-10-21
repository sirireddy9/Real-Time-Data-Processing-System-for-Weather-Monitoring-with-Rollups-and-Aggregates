import requests
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to store daily weather summary in the database
def store_daily_summary(city, avg_temp, max_temp, min_temp, weather_condition):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()

    # Use the current date
    date = datetime.now().strftime("%Y-%m-%d")

    # Insert the data into the table
    c.execute('''INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_weather)
                 VALUES (?, ?, ?, ?, ?, ?)''', 
                 (city, date, avg_temp, max_temp, min_temp, weather_condition))

    conn.commit()
    conn.close()

# Function to fetch weather data for a given city
def get_weather_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    # Log request details and check for a valid response
    print(f"Fetching weather data for {city}...")
    print(f"Request URL: {url}")
    print(f"Response Status Code: {response.status_code}")

    if response.status_code == 200:
        print(f"Weather data received for {city}.")
        return response.json()
    else:
        print(f"Failed to fetch weather data for {city}. Error: {response.text}")
        return None

# Main function to process multiple cities
def fetch_and_store_weather():
    # Load the OpenWeather API key from the environment variable
    api_key = os.getenv('OPENWEATHER_API_KEY')

    if not api_key:
        print("API key not found. Please check your .env file.")
        return

    # List of cities to fetch weather for
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

    for city in cities:
        data = get_weather_data(city, api_key)
        if data:
            # Extract necessary weather details from the API response
            avg_temp = data['main']['temp']
            max_temp = data['main']['temp_max']
            min_temp = data['main']['temp_min']
            weather_condition = data['weather'][0]['main']

            # Store the fetched weather data in the database
            store_daily_summary(city, avg_temp, max_temp, min_temp, weather_condition)
            print(f"Weather data for {city} stored successfully.")
        else:
            print(f"Failed to fetch or store weather data for {city}.")

# Call the main function to fetch and store weather data
fetch_and_store_weather()
