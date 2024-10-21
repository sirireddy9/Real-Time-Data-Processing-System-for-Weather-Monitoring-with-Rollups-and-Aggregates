import matplotlib.pyplot as plt
import sqlite3

# Function to plot temperature trends for multiple cities
def plot_temperature_trends(cities):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    
    for city in cities:
        # Fetch temperature data for each city
        c.execute('''SELECT date, avg_temp FROM daily_summary WHERE city = ? ORDER BY date''', (city,))
        results = c.fetchall()
        
        if results:
            dates = [row[0] for row in results]
            temps = [row[1] for row in results]
            
            # Plot temperature trend for the city
            plt.plot(dates, temps, label=city)
        else:
            print(f"No data available for {city}")
    
    conn.close()
    
    # Add titles and labels to the plot
    plt.title("Temperature Trends for Multiple Cities")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()  # Show legend to differentiate between cities
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to avoid overlap
    plt.show()

# List of cities to plot temperature trends for
cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

# Call the function to plot temperature trends for all cities
plot_temperature_trends(cities)
