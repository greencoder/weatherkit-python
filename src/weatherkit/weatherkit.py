import arrow
import cryptography
import json
import jwt
import requests

from .models import CurrentConditions
from .models import DailyForecast
from .models import NextHourForecast
from .models import HourlyForecast
from .models import WeatherKitResponse


class WeatherKit():

    def __init__(self, team_id, service_id, private_key, key_id):
        self.token = self._create_jwt(team_id, service_id, private_key, key_id)

    def _create_jwt(self, team_id, service_id, private_key, key_id):
        """ Creates the JWT for the WeatherKit API Request """
        init_at = int(arrow.now().timestamp())
        expire_at = int(arrow.now().shift(hours=1).timestamp())

        token = jwt.encode(
            payload = {
                'iss': team_id,
                'sub': service_id,
                'iat': init_at,
                'exp': expire_at,
            },
            key = private_key,
            headers = {
                'alg': 'ES256',
                'kid': key_id,
                'typ': 'JWT',
                'id': f'{team_id}.{service_id}'
            }
        )

        return token

    def _fetch_api(self, forecast_datasets, latitude, longitude, country_code, timezone):
        """ Fetches the weather from the WeatherKit API """
        url = f'https://weatherkit.apple.com/api/v1/weather/en/{latitude}/{longitude}'
        headers = {'Authorization': f'Bearer {self.token}'}

        params = {
            'countryCode': country_code,
            'timezone': timezone,
            'dataSets': ','.join(forecast_datasets),
        }

        response = requests.get(url, params=params, headers=headers)
        assert response.ok, 'Could not fetch data'
        return response.json()

    def fetch(self, forecast_datasets, latitude, longitude, country_code, timezone):
        """ Fetches and parses the weather from the WeatherKit API """
        data = self._fetch_api(forecast_datasets, latitude, longitude, country_code, timezone)

        response = WeatherKitResponse()

        if 'currentWeather' in data.keys():
            raw_current_conditions = data.get('currentWeather', {})
            response.current_weather = CurrentConditions(raw_current_conditions, timezone)

        if 'forecastNextHour' in data.keys():
            raw_next_hour_forecast = data.get('forecastNextHour', {})
            next_hour_forecast = NextHourForecast(raw_next_hour_forecast, timezone)
            response.forecast_next_hour = next_hour_forecast

        if 'forecastHourly' in data.keys():
            raw_hourly_forecasts = data.get('forecastHourly', {}).get('hours', [])
            hourly_forecasts = [HourlyForecast(h, timezone) for h in raw_hourly_forecasts]
            response.forecast_hourly = hourly_forecasts

        if 'forecastDaily' in data.keys():
            raw_daily_forecasts = data.get('forecastDaily', {}).get('days', [])
            daily_forecasts = [DailyForecast(d, timezone) for d in raw_daily_forecasts]
            response.forecast_daily = daily_forecasts

        return response
