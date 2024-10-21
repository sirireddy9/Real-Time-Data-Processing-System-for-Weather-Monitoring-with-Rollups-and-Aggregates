import sqlite3

# Connect to SQLite database (it will create one if it doesn't exist)
conn = sqlite3.connect('weather_data.db')
c = conn.cursor()

# Create table for daily summaries
c.execute('''CREATE TABLE IF NOT EXISTS daily_summary (
             city TEXT, date TEXT, avg_temp REAL, max_temp REAL, min_temp REAL, dominant_weather TEXT)''')

conn.commit()
conn.close()
