# weatherkit-python
A Python wrapper for Apple's WeatherKit API

# Installation
You can install the WeatherKit library from PyPI:

```
$ pip install weatherkit-python
```

The library is supported on Python 3.6 and above.

# Dependencies

The following dependencies are installed with the library:

* [Arrow](https://github.com/arrow-py/arrow)
* [Cryptography](https://github.com/pyca/cryptography)
* [PyJWT](https://github.com/jpadilla/pyjwt)
* [Requests](https://github.com/psf/requests)

# JSON Web Token Generation

The library will take care of JWT generation for you since it's such a pain. The expiration time for the token is one hour after generation.

# Dates and Timezones

The library will convert all datetime values to the timezone of your choosing. You can specify `UTC` to return GMT datetimes. All values are returned in ISO8106 format.

# Unit Conversion

The Apple WeatherKit APIs only return values in metric units, but the library also adds imperial properties for all values. All temperatures have both Fahrenheit and Celsius properties. See the API docs for all available object properties.

# Conditions

The Apple APIs return `conditionCode` values that are automatically mapped to human-readable conditions strings. The available conditions are:

|**Code**|**Condition**|
|--------|-------------|
|Clear|Clear|
|Cloudy|Cloudy|
|Dust|Dust|
|Fog|Fog|
|Haze|Haze|
|MostlyClear|Mostly Clear|
|MostlyCloudy|Mostly Cloudy|
|PartlyCloudy|Partly Cloudy|
|ScatteredThunderstorms|Scattered Thunderstorms|
|Smoke|Smoke|
|Breezy|Breezy|
|Windy|Windy|
|Drizzle|Drizzle|
|HeavyRain|Heavy Rain|
|Rain|Rain|
|Showers|Showers|
|Flurries|Flurries|
|HeavySnow|Heavy Snow|
|MixedRainAndSleet|Mixed Rain and Sleet|
|MixedRainAndSnow|Mixed Rain and Snow|
|MixedRainfall|Mixed Rainfall|
|MixedSnowAndSleet|Mixed Snow and Sleet|
|ScatteredShowers|Scattered Showers|
|ScatteredSnowShowers|Scattered Snow Showers|
|Sleet|Sleet|
|Snow|Snow|
|SnowShowers|Snow Showers|
|Blizzard|Blizzard|
|BlowingSnow|Blowing Snow|
|FreezingDrizzle|Freezing Drizzle|
|FreezingRain|Freezing Rain|
|Frigid|Frigid|
|Hail|Hail|
|Hot|Hot|
|Hurricane|Hurricane|
|IsolatedThunderstorms|Isolated Thunderstorms|
|SevereThunderstorm|Severe Thunderstorm|
|Thunderstorm|Thunderstorm|
|Tornado|Tornado|
|TropicalStorm|Tropical Storm|

# Precip Types

The `DailyForecast`, `NextHourForecast`, and `HourlyForecast` objects have a `precip_type` string that can have the following values:

|**type**|**description**|
|----|-----------|
|hail|A form of precipitation consisting of solid ice]
|mixed|Mixed precipitation|
|rain|Rain|
|sleet|A form of precipitation consisting of ice pellets|
|snow|Snow|
|none|No precipitation|


# How to Use

```
import os
import json
import weatherkit

# Load the credentials from wherever you store them securely
team_id = os.environ.get('APPLE_TEAM_ID')
key_id = os.environ.get('APPLE_KEY_ID')
service_id = os.environ.get('APPLE_SERVICE_ID')
private_key = os.environ.get('APPLE_PRIVATE_KEY')

# Instantiate the WeatherKit object
wk_client = weatherkit.WeatherKit(team_id, service_id, private_key, key_id)

# Include any/all of the datasets we want to pull in the list
datasets = [
    'forecastHourly',
    'forecastDaily',
    'currentWeather',
    'forecastNextHour',
]

# Fetch the API
forecasts = wk_client.fetch(datasets, 39.5900, -104.726763, 'US', 'US/Mountain')

# There is a convenience method for converting the forecast response object to JSON
forecasts_json = forecasts.as_json()
```

# Running the tests

From the `/weatherkit` directory:
```
$ python -m unittest tests/tests.py
```

# Contributions

Pull requests are welcome so long as they do not add unnecessary complexity to the user.
