import os
import json
import pathlib
import unittest
import sys

from models import CurrentConditions
from models import DailyForecast
from models import HourlyForecast
from models import NextHourForecast
from models import Weather


class TestUnitConversions(unittest.TestCase):

    def setUp(self):
        self.weather = Weather()

    def test_conversions(self):
        self.assertEqual(self.weather.millimeters_to_inches(25.4), 1)
        self.assertEqual(self.weather.celsius_to_fahrenheit(17.7778), 64.00004)
        self.assertEqual(self.weather.degrees_to_cardinal(0), 'N')
        self.assertEqual(self.weather.kmh_to_mph(11), 6.8354)
        self.assertEqual(self.weather.meters_to_miles(17702.8), 11.0000099377376)


class TextNextHourForecast(unittest.TestCase):

    def setUp(self):
        api_data = json.loads(pathlib.Path('tests/sample_data.json').read_text())
        raw_next_hour_forecast = api_data.get('forecastNextHour', {})
        next_hour_forecast = NextHourForecast(raw_next_hour_forecast, 'US/Mountain')
        self.next_hour_forecast = next_hour_forecast

    def test_parsing(self):
        self.assertEqual(self.next_hour_forecast.start_datetime, '2022-11-18T09:34:00-07:00')
        self.assertEqual(self.next_hour_forecast.precip_type, 'clear')
        self.assertEqual(self.next_hour_forecast.precip_chance, 0.0)
        self.assertEqual(self.next_hour_forecast.precip_intensity, 0.0)
        self.assertEqual(self.next_hour_forecast.minutes[0].start_datetime, '2022-11-18T09:34:00-07:00')
        self.assertEqual(self.next_hour_forecast.minutes[0].precip_chance, 0.0)
        self.assertEqual(self.next_hour_forecast.minutes[0].precip_intensity, 0.0)


class TestDailyForecasts(unittest.TestCase):

    def setUp(self):
        api_data = json.loads(pathlib.Path('tests/sample_data.json').read_text())
        raw_forecasts = api_data.get('forecastDaily', {}).get('days', [])
        daily_forecasts = [DailyForecast(d, 'US/Mountain') for d in raw_forecasts]
        self.forecast = daily_forecasts[0]

    def test_parsing(self):
        self.assertEqual(self.forecast.start_datetime, '2022-11-18T00:00:00-07:00')
        self.assertEqual(self.forecast.end_datetime, '2022-11-19T00:00:00-07:00')
        self.assertEqual(self.forecast.condition_code, 'PartlyCloudy')
        self.assertEqual(self.forecast.conditions, 'Partly Cloudy')
        self.assertEqual(self.forecast.icon, 'partlycloudy.svg')
        self.assertEqual(self.forecast.max_uv_index, 2)
        self.assertEqual(self.forecast.moon_phase, 'thirdQuarter')
        self.assertEqual(self.forecast.precip_amount_mm, 0.0)
        self.assertEqual(self.forecast.precip_amount_in, 0.0)
        self.assertEqual(self.forecast.precip_chance, 0.28)
        self.assertEqual(self.forecast.precip_type, 'clear')
        self.assertEqual(self.forecast.snowfall_amount_mm, 0.0)
        self.assertEqual(self.forecast.snowfall_amount_in, 0.0)
        self.assertEqual(self.forecast.sunrise, '2022-11-18T06:46:43-07:00')
        self.assertEqual(self.forecast.sunset, '2022-11-18T16:41:27-07:00')
        self.assertEqual(self.forecast.temperature_max_c, -3.56)
        self.assertEqual(self.forecast.temperature_min_c, -13.43)
        self.assertEqual(self.forecast.temperature_max_f, 25.592)
        self.assertEqual(self.forecast.temperature_min_f, 7.8260000000000005)

        self.assertEqual(self.forecast.daytime_cloud_cover, 0.3)
        self.assertEqual(self.forecast.daytime_condition_code, 'MostlyClear')
        self.assertEqual(self.forecast.daytime_conditions, 'Mostly Clear')
        self.assertEqual(self.forecast.daytime_humidity, 0.67)
        self.assertEqual(self.forecast.daytime_icon, 'mostlyclear.svg')
        self.assertEqual(self.forecast.daytime_precip_amount_mm, 0.0)
        self.assertEqual(self.forecast.daytime_precip_amount_in, 0.0)
        self.assertEqual(self.forecast.daytime_precip_chance, 0.1)
        self.assertEqual(self.forecast.daytime_precip_type, 'clear')
        self.assertEqual(self.forecast.daytime_snowfall_amount_mm, 0.0)
        self.assertEqual(self.forecast.daytime_snowfall_amount_in, 0.0)
        self.assertEqual(self.forecast.daytime_wind_degrees, 89)
        self.assertEqual(self.forecast.daytime_wind_direction, 'E')
        self.assertEqual(self.forecast.daytime_wind_speed_avg_kmh, 5.33)
        self.assertEqual(self.forecast.daytime_wind_speed_avg_mph, 3.3120619999999996)

        self.assertEqual(self.forecast.overnight_cloud_cover, 0.04)
        self.assertEqual(self.forecast.overnight_condition_code, 'MostlyClear')
        self.assertEqual(self.forecast.overnight_conditions, 'Mostly Clear')
        self.assertEqual(self.forecast.overnight_humidity, 0.72)
        self.assertEqual(self.forecast.overnight_icon, 'mostlyclear.svg')
        self.assertEqual(self.forecast.overnight_precip_amount_mm, 0.0)
        self.assertEqual(self.forecast.overnight_precip_amount_in, 0.0)
        self.assertEqual(self.forecast.overnight_precip_chance, 0.01)
        self.assertEqual(self.forecast.overnight_precip_type, 'clear')
        self.assertEqual(self.forecast.overnight_snowfall_amount_mm, 0.0)
        self.assertEqual(self.forecast.overnight_snowfall_amount_in, 0.0)
        self.assertEqual(self.forecast.overnight_wind_degrees, 189)
        self.assertEqual(self.forecast.overnight_wind_direction, 'S')
        self.assertEqual(self.forecast.overnight_wind_speed_avg_kmh, 10.11)
        self.assertEqual(self.forecast.overnight_wind_speed_avg_mph, 6.282353999999999)

        self.assertEqual(self.forecast.nighttime_cloud_cover, 0.12)
        self.assertEqual(self.forecast.nighttime_condition_code, 'MostlyCloudy')
        self.assertEqual(self.forecast.nighttime_conditions, 'Mostly Cloudy')
        self.assertEqual(self.forecast.nighttime_humidity, 0.67)
        self.assertEqual(self.forecast.nighttime_icon, 'mostlycloudy.svg')
        self.assertEqual(self.forecast.nighttime_precip_amount_mm, 0.0)
        self.assertEqual(self.forecast.nighttime_precip_amount_in, 0.0)
        self.assertEqual(self.forecast.nighttime_precip_chance, 0.06)
        self.assertEqual(self.forecast.nighttime_precip_type, 'clear')
        self.assertEqual(self.forecast.nighttime_snowfall_amount_mm, 0.0)
        self.assertEqual(self.forecast.nighttime_snowfall_amount_in, 0.0)
        self.assertEqual(self.forecast.nighttime_wind_degrees, 172)
        self.assertEqual(self.forecast.nighttime_wind_direction, 'S')
        self.assertEqual(self.forecast.nighttime_wind_speed_avg_kmh, 6.67)
        self.assertEqual(self.forecast.nighttime_wind_speed_avg_mph, 4.144737999999999)


class TestHourlyForecasts(unittest.TestCase):

    def setUp(self):
        api_data = json.loads(pathlib.Path('tests/sample_data.json').read_text())
        raw_forecasts = api_data.get('forecastHourly', {}).get('hours', [])
        hourly_forecasts = [HourlyForecast(h, 'US/Mountain') for h in raw_forecasts]
        self.forecast = hourly_forecasts[0]

    def test_parsing(self):
        self.assertEqual(self.forecast.start_datetime, '2022-11-17T22:00:00-07:00')
        self.assertEqual(self.forecast.end_datetime, '2022-11-17T23:00:00-07:00')
        self.assertEqual(self.forecast.cloud_cover, 0.96)
        self.assertEqual(self.forecast.condition_code, 'MostlyCloudy')
        self.assertEqual(self.forecast.conditions, 'Mostly Cloudy')
        self.assertEqual(self.forecast.icon, 'mostlycloudy.svg')
        self.assertEqual(self.forecast.is_daylight, False)
        self.assertEqual(self.forecast.humidity, 0.87)
        self.assertEqual(self.forecast.precip_amount_mm, 0.0)
        self.assertEqual(self.forecast.precip_amount_inches, 0.0)
        self.assertEqual(self.forecast.precip_intensity, 0.0)
        self.assertEqual(self.forecast.precip_chance, 0.0)
        self.assertEqual(self.forecast.precip_type, 'clear')
        self.assertEqual(self.forecast.pressure_mb, 1036.07)
        self.assertEqual(self.forecast.pressure_trend, 'rising')
        self.assertEqual(self.forecast.snowfall_intensity, 0.0)
        self.assertEqual(self.forecast.snowfall_amount_mm, 0.0)
        self.assertEqual(self.forecast.snowfall_amount_inches, 0.0)
        self.assertEqual(self.forecast.temperature_c, -10.36)
        self.assertEqual(self.forecast.temperature_f, 13.352)
        self.assertEqual(self.forecast.temperature_feels_like_c, -15.9)
        self.assertEqual(self.forecast.temperature_feels_like_f, 3.3800000000000026)
        self.assertEqual(self.forecast.temperature_dew_point_c, -12.16)
        self.assertEqual(self.forecast.temperature_dew_point_f, 10.112000000000002)
        self.assertEqual(self.forecast.uv_index, 0)
        self.assertEqual(self.forecast.visibility_meters, 7340.88)
        self.assertEqual(self.forecast.visibility_miles, 4.56141135592896)
        self.assertEqual(self.forecast.wind_degrees, 81)
        self.assertEqual(self.forecast.wind_direction, 'E')
        self.assertEqual(self.forecast.wind_gust_kmh, 17.49)
        self.assertEqual(self.forecast.wind_gust_mph, 10.868285999999998)
        self.assertEqual(self.forecast.wind_speed_kmh, 10.61)
        self.assertEqual(self.forecast.wind_speed_mph, 6.5930539999999995)


class TestCurrentConditions(unittest.TestCase):

    def setUp(self):
        api_data = json.loads(pathlib.Path('tests/sample_data.json').read_text())
        raw_conditions_data = api_data.get('currentWeather')
        self.current_conditions = CurrentConditions(raw_conditions_data, 'US/Mountain')

    def test_parsing(self):
        self.assertEqual(self.current_conditions.current_datetime, '2022-11-18T09:34:14-07:00')
        self.assertEqual(self.current_conditions.cloud_cover, 0.61)
        self.assertEqual(self.current_conditions.condition_code, 'PartlyCloudy')
        self.assertEqual(self.current_conditions.conditions, 'Partly Cloudy')
        self.assertEqual(self.current_conditions.icon, 'partlycloudy.svg')
        self.assertEqual(self.current_conditions.is_daylight, True)
        self.assertEqual(self.current_conditions.humidity, 0.75)
        self.assertEqual(self.current_conditions.precip_intensity, 0.0)
        self.assertEqual(self.current_conditions.pressure_mb, 1035.14)
        self.assertEqual(self.current_conditions.pressure_trend, 'falling')
        self.assertEqual(self.current_conditions.temperature_c, -9.57)
        self.assertEqual(self.current_conditions.temperature_f, 14.774000000000001)
        self.assertEqual(self.current_conditions.temperature_feels_like_c, -13.07)
        self.assertEqual(self.current_conditions.temperature_feels_like_f, 8.474)
        self.assertEqual(self.current_conditions.temperature_dew_point_c, -13.18)
        self.assertEqual(self.current_conditions.temperature_dew_point_f, 8.276)
        self.assertEqual(self.current_conditions.uv_index, 2)
        self.assertEqual(self.current_conditions.visibility_meters, 25447.71)
        self.assertEqual(self.current_conditions.visibility_miles, 15.812473896370319)
        self.assertEqual(self.current_conditions.wind_degrees, 161)
        self.assertEqual(self.current_conditions.wind_direction, 'SSE')
        self.assertEqual(self.current_conditions.wind_gust_kmh, 14.07)
        self.assertEqual(self.current_conditions.wind_gust_mph, 8.743098)
        self.assertEqual(self.current_conditions.wind_speed_kmh, 6.07)
        self.assertEqual(self.current_conditions.wind_speed_mph, 3.7718979999999998)


if __name__ == '__main__':
    unittest.main()
