from datetime import datetime
import sqlite3

def store_daily_summary(city, avg_temp, max_temp, min_temp, weather_condition):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()

    date = datetime.now().strftime("%Y-%m-%d")
    c.execute('''INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_weather)
                 VALUES (?, ?, ?, ?, ?, ?)''', (city, date, avg_temp, max_temp, min_temp, weather_condition))

    conn.commit()
    conn.close()

# Example usage - Insert data for a city (e.g., Delhi)
city = "Delhi"
avg_temp = 28.5  # Sample data for demonstration
max_temp = 32.1
min_temp = 25.0
dominant_weather = "Clear"

# Store the data in the database
store_daily_summary(city, avg_temp, max_temp, min_temp, dominant_weather)
