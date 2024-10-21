import requests
import sqlite3
import time
import os
from datetime import datetime
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# Load environment variables from .env file
load_dotenv()

# Database setup
def setup_database():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            date TEXT,
            avg_temp REAL,
            max_temp REAL,
            min_temp REAL,
            dominant_weather TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to store daily weather summary
def store_daily_summary(city, avg_temp, max_temp, min_temp, weather_condition):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    c.execute('''INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_weather)
                 VALUES (?, ?, ?, ?, ?, ?)''', 
                 (city, date, avg_temp, max_temp, min_temp, weather_condition))
    conn.commit()
    conn.close()

# Function to fetch weather data
def get_weather_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch weather data for {city}. Error: {response.text}")
        return None

# Function to check for alerts
def check_alerts(city, temp):
    threshold = 35
    if temp > threshold:
        print(f"Alert: {city} has exceeded the threshold temperature of {threshold}°C with {temp}°C!")

# Visualization function
def plot_temperature_trends():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
    for city in cities:
        c.execute('''SELECT date, avg_temp FROM daily_summary WHERE city = ?''', (city,))
        results = c.fetchall()
        
        dates = [row[0] for row in results]
        temps = [row[1] for row in results]
        
        plt.plot(dates, temps, label=city)

    plt.title(f"Temperature Trends")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.show()

# Main function
def main():
    setup_database()
    
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        print("Error: No API key found! Please set the 'OPENWEATHER_API_KEY' environment variable.")
        return
    
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
    
    while True:
        for city in cities:
            data = get_weather_data(city, api_key)
            if data:
                avg_temp = data['main']['temp']
                max_temp = data['main']['temp_max']
                min_temp = data['main']['temp_min']
                weather_condition = data['weather'][0]['main']
                
                store_daily_summary(city, avg_temp, max_temp, min_temp, weather_condition)
                print(f"Weather data for {city} stored successfully.")
                
                check_alerts(city, avg_temp)
            else:
                print(f"No weather data available for {city}")
        
        time.sleep(300)  # 5-minute interval

# Run the program
if __name__ == '__main__':
    main()
    plot_temperature_trends()
