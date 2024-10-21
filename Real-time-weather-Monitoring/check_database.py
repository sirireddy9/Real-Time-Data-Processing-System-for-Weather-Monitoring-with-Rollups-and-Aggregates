import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')
c = conn.cursor()

# Query to check the table
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()

print("Tables in the database:", tables)

conn.close()
