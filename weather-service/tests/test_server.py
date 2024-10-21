import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime, timedelta

from weather_service.utils import fetch_weather_data, check_data_against_alerts, Thresholds
from weather_service.db_utils import insert_realtime_weather, aggregate_daily_weather, get_alerts
from weather_service.main import CITIES, API_URL, OPENWEATHER_API_KEY

class APITestHandler(unittest.IsolatedAsyncioTestCase):

    @patch('weather_service.utils.requests.get')
    async def test_system_setup(self, mock_get):
        # Simulate a successful API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = MagicMock(return_value={
            'dt': 1627635600,
            'weather': [{'main': 'Clear'}],
            'main': {
                'temp': 300,
                'feels_like': 300,
                'pressure': 1013,
                'humidity': 40
            },
            'rain': {'1h': 0},
            'clouds': {'all': 0}
        })

        for city in CITIES:
            weather_data = await fetch_weather_data(API_URL, OPENWEATHER_API_KEY, city)
            self.assertIsNotNone(weather_data)

    @patch('weather_service.utils.requests.get')
    async def test_data_retrieval(self, mock_get):
        # Simulate a successful API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = MagicMock(return_value={
            'dt': 1627635600,
            'weather': [{'main': 'Clear'}],
            'main': {
                'temp': 300,
                'feels_like': 300,
                'pressure': 1013,
                'humidity': 40
            },
            'rain': {'1h': 0},
            'clouds': {'all': 0}
        })

        for city in CITIES:
            weather_data = await fetch_weather_data(API_URL, OPENWEATHER_API_KEY, city)
            self.assertIsNotNone(weather_data)
            self.assertEqual(weather_data['main_condition'], 'Clear')

    def test_temperature_conversion(self):
        # Test Kelvin to Celsius conversion
        temp_kelvin = 300
        temp_celsius = temp_kelvin - 273.15
        self.assertAlmostEqual(temp_celsius, 26.85, places=2)

    @patch('weather_service.db_utils.session')
    def test_daily_weather_summary(self, mock_session):
        mock_session.query.return_value.filter.return_value.all.return_value = [
            {
                'city': 'Delhi',
                'date': datetime.utcnow().date(),
                'avg_temp': 30,
                'max_temp': 35,
                'min_temp': 25,
                'dom_condition': 'Clear'
            }
        ]
        
        aggregate_daily_weather()

        mock_session.merge.assert_called()

    @patch('weather_service.utils.insert_alert_event')
    def test_alerting_thresholds(self, mock_insert_alert_event):
        thresholds = Thresholds(temp=[20, 30], feels_like=[20, 30], pressure=[1000, 1020], humidity=[30, 50], rain=[0, 5], clouds=[0, 50])

        weather_data = {
            'dt': datetime.utcnow(),
            'main_condition': 'Clear',
            'temp': 35,  # Exceeds the threshold
            'feels_like': 35,  # Exceeds the threshold
            'pressure': 1010,
            'humidity': 40,
            'rain': 0,
            'clouds': 0,
            'city': 'Delhi'
        }

        check_data_against_alerts(weather_data, thresholds.get_thresholds())

        self.assertTrue(mock_insert_alert_event.called)

if __name__ == '__main__':
    unittest.main()
