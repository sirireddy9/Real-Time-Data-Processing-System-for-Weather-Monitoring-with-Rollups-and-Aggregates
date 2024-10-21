from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENWEATHER_API_KEY')

if api_key:
    print(f"Your API key is: {api_key}")
else:
    print("API key not found. Make sure it's in your .env file.")
