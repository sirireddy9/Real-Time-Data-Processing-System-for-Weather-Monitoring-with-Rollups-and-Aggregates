import sqlite3
def get_daily_summary():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()

    c.execute('''SELECT city, date, AVG(avg_temp), MAX(max_temp), MIN(min_temp), dominant_weather
                 FROM daily_summary
                 GROUP BY city, date''')
    
    results = c.fetchall()
    conn.close()
    
    for row in results:
        print(f"City: {row[0]}, Date: {row[1]}, Avg Temp: {row[2]}, Max Temp: {row[3]}, Min Temp: {row[4]}, Weather: {row[5]}")

get_daily_summary()
