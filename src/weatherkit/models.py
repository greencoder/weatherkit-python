import arrow
import jsonpickle


class Weather():

    def millimeters_to_inches(self, mm_value):
        if mm_value is None: return None
        return mm_value / 25.4

    def celsius_to_fahrenheit(self, c_value):
        if c_value is None: return None
        return (c_value * 9/5) + 32

    def degrees_to_cardinal(self, d_value):
        if d_value is None: return None
        dirs = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
        ix = round(d_value / (360.0 / len(dirs)))
        return dirs[ix % len(dirs)]

    def kmh_to_mph(self, kmh_value):
        if kmh_value is None: return None
        return 0.6214 * kmh_value

    def icon_for_condition_code(self, code):
        if not code or code == '':
            return 'unknown.svg'
        else:
            return code.lower() + '.svg'

    def meters_to_miles(self, m_value):
        if m_value is None: return None
        return m_value * 0.000621371192

    def conditions_for_code(self, code):
        if not code or code == '': return None

        codes = {
            'Clear': 'Clear',
            'Cloudy': 'Cloudy',
            'Dust': 'Dust',
            'Fog': 'Fog',
            'Haze': 'Haze',
            'MostlyClear': 'Mostly Clear',
            'MostlyCloudy': 'Mostly Cloudy',
            'PartlyCloudy': 'Partly Cloudy',
            'ScatteredThunderstorms': 'Scattered Thunderstorms',
            'Smoke': 'Smoke',
            'Breezy': 'Breezy',
            'Windy': 'Windy',
            'Drizzle': 'Drizzle',
            'HeavyRain': 'Heavy Rain',
            'Rain': 'Rain',
            'Showers': 'Showers',
            'Flurries': 'Flurries',
            'HeavySnow': 'Heavy Snow',
            'MixedRainAndSleet': 'Mixed Rain and Sleet',
            'MixedRainAndSnow': 'Mixed Rain and Snow',
            'MixedRainfall': 'Mixed Rainfall',
            'MixedSnowAndSleet': 'Mixed Snow and Sleet',
            'ScatteredShowers': 'Scattered Showers',
            'ScatteredSnowShowers': 'Scattered Snow Showers',
            'Sleet': 'Sleet',
            'Snow': 'Snow',
            'SnowShowers': 'Snow Showers',
            'Blizzard': 'Blizzard',
            'BlowingSnow': 'Blowing Snow',
            'FreezingDrizzle': 'Freezing Drizzle',
            'FreezingRain': 'Freezing Rain',
            'Frigid': 'Frigid',
            'Hail': 'Hail',
            'Hot': 'Hot',
            'Hurricane': 'Hurricane',
            'IsolatedThunderstorms': 'Isolated Thunderstorms',
            'SevereThunderstorm': 'Severe Thunderstorm',
            'Thunderstorm': 'Thunderstorm',
            'Tornado': 'Tornado',
            'TropicalStorm': 'Tropical Storm',
        }

        return codes.get(code, 'Unknown')


class MinuteForecast(Weather):

    def __init__(self, data, timezone):
        self.start_datetime = arrow.get(data.get('startTime')).to(timezone).for_json()
        self.precip_chance = data.get('precipitationChance')
        self.precip_intensity = data.get('precipitationIntensity')


class NextHourForecast(Weather):

    def __init__(self, data, timezone):
        self.start_datetime = None
        self.precip_type = None
        self.precip_chance = None
        self.precip_intensity = None
        self.minutes = []

        summaries = data.get('summary', [])

        if len(summaries) > 0:
            summary = summaries[0]
            self.start_datetime = arrow.get(summary.get('startTime')).to(timezone).for_json()
            self.precip_type = summary.get('condition') # Note this is called "condition" in the API
            self.conditions = self.conditions_for_code(self.condition_code)
            self.precip_chance = summary.get('precipitationChance')
            self.precip_intensity = summary.get('precipitationIntensity')
            self.minutes = [MinuteForecast(m, timezone) for m in data.get('minutes')]


class CurrentConditions(Weather):

    def __init__(self, data, timezone):
        self.current_datetime = arrow.get(data.get('asOf')).to(timezone).for_json()
        self.cloud_cover = data.get('cloudCover')
        self.condition_code = data.get('conditionCode')
        self.conditions = self.conditions_for_code(self.condition_code)
        self.icon = self.icon_for_condition_code(self.condition_code)
        self.is_daylight = data.get('daylight')
        self.humidity = data.get('humidity')
        self.precip_intensity = data.get('precipitationIntensity')
        self.pressure_mb = data.get('pressure')
        self.pressure_trend = data.get('pressureTrend')
        self.temperature_c = data.get('temperature')
        self.temperature_f = self.celsius_to_fahrenheit(self.temperature_c)
        self.temperature_feels_like_c = data.get('temperatureApparent')
        self.temperature_feels_like_f = self.celsius_to_fahrenheit(self.temperature_feels_like_c)
        self.temperature_dew_point_c = data.get('temperatureDewPoint')
        self.temperature_dew_point_f = self.celsius_to_fahrenheit(self.temperature_dew_point_c)
        self.uv_index = data.get('uvIndex')
        self.visibility_meters = data.get('visibility')
        self.visibility_miles = self.meters_to_miles(self.visibility_meters)
        self.wind_degrees = data.get('windDirection')
        self.wind_direction = self.degrees_to_cardinal(self.wind_degrees)
        self.wind_gust_kmh = data.get('windGust')
        self.wind_gust_mph = self.kmh_to_mph(self.wind_gust_kmh)
        self.wind_speed_kmh = data.get('windSpeed')
        self.wind_speed_mph = self.kmh_to_mph(self.wind_speed_kmh)

    def default(self, obj):
        return obj.__dict__


class HourlyForecast(Weather):

    def __init__(self, data, timezone):
        self.start_datetime = arrow.get(data.get('forecastStart')).to(timezone).for_json()
        self.end_datetime = arrow.get(data.get('forecastStart')).shift(hours=1).to(timezone).for_json()
        self.cloud_cover = data.get('cloudCover')
        self.condition_code = data.get('conditionCode')
        self.conditions = self.conditions_for_code(self.condition_code)
        self.icon = self.icon_for_condition_code(self.condition_code)
        self.is_daylight = data.get('daylight')
        self.humidity = data.get('humidity')
        self.precip_amount_mm = data.get('precipitationAmount')
        self.precip_amount_inches = self.millimeters_to_inches(self.precip_amount_mm)
        self.precip_intensity = data.get('precipitationIntensity')
        self.precip_chance = data.get('precipitationChance')
        self.precip_type = data.get('precipitationType')
        self.pressure_mb = data.get('pressure')
        self.pressure_trend = data.get('pressureTrend')
        self.snowfall_intensity = data.get('snowfallIntensity')
        self.snowfall_amount_mm = data.get('snowfallAmount')
        self.snowfall_amount_inches = self.millimeters_to_inches(self.snowfall_amount_mm)
        self.temperature_c = data.get('temperature')
        self.temperature_f = self.celsius_to_fahrenheit(self.temperature_c)
        self.temperature_feels_like_c = data.get('temperatureApparent')
        self.temperature_feels_like_f = self.celsius_to_fahrenheit(self.temperature_feels_like_c)
        self.temperature_dew_point_c = data.get('temperatureDewPoint')
        self.temperature_dew_point_f = self.celsius_to_fahrenheit(self.temperature_dew_point_c)
        self.uv_index = data.get('uvIndex')
        self.visibility_meters = data.get('visibility')
        self.visibility_miles = self.meters_to_miles(self.visibility_meters)
        self.wind_degrees = data.get('windDirection')
        self.wind_direction = self.degrees_to_cardinal(self.wind_degrees)
        self.wind_gust_kmh = data.get('windGust')
        self.wind_gust_mph = self.kmh_to_mph(self.wind_gust_kmh)
        self.wind_speed_kmh = data.get('windSpeed')
        self.wind_speed_mph = self.kmh_to_mph(self.wind_speed_kmh)


class DailyForecast(Weather):

    def __init__(self, data, timezone):
        self.start_datetime = arrow.get(data.get('forecastStart')).to(timezone).for_json()
        self.end_datetime = arrow.get(data.get('forecastEnd')).to(timezone).for_json()
        self.condition_code = data.get('conditionCode')
        self.conditions = self.conditions_for_code(self.condition_code)
        self.icon = self.icon_for_condition_code(self.condition_code)
        self.max_uv_index = data.get('maxUvIndex')
        self.moon_phase = data.get('moonPhase')
        self.precip_amount_mm = data.get('precipitationAmount')
        self.precip_amount_in = self.millimeters_to_inches(self.precip_amount_mm)
        self.precip_chance = data.get('precipitationChance')
        self.precip_type = data.get('precipitationType')
        self.snowfall_amount_mm = data.get('snowfallAmount')
        self.snowfall_amount_in = self.millimeters_to_inches(self.snowfall_amount_mm)
        self.sunrise = arrow.get(data.get('sunrise')).to(timezone).for_json()
        self.sunset = arrow.get(data.get('sunset')).to(timezone).for_json()
        self.temperature_max_c = data.get('temperatureMax')
        self.temperature_min_c = data.get('temperatureMin')
        self.temperature_max_f = self.celsius_to_fahrenheit(self.temperature_max_c)
        self.temperature_min_f = self.celsius_to_fahrenheit(self.temperature_min_c)

        self.daytime_cloud_cover = data.get('daytimeForecast', {}).get('cloudCover')
        self.daytime_condition_code = data.get('daytimeForecast', {}).get('conditionCode')
        self.daytime_conditions = self.conditions_for_code(self.daytime_condition_code)
        self.daytime_icon = self.icon_for_condition_code(self.daytime_condition_code)
        self.daytime_humidity = data.get('daytimeForecast', {}).get('humidity')
        self.daytime_precip_amount_mm = data.get('daytimeForecast', {}).get('precipitationAmount')
        self.daytime_precip_amount_in = self.millimeters_to_inches(self.daytime_precip_amount_mm)
        self.daytime_precip_chance = data.get('daytimeForecast', {}).get('precipitationChance')
        self.daytime_precip_type = data.get('daytimeForecast', {}).get('precipitationType')
        self.daytime_snowfall_amount_mm = data.get('daytimeForecast', {}).get('snowfallAmount')
        self.daytime_snowfall_amount_in = self.millimeters_to_inches(self.daytime_snowfall_amount_mm)
        self.daytime_wind_degrees = data.get('daytimeForecast', {}).get('windDirection')
        self.daytime_wind_direction = self.degrees_to_cardinal(self.daytime_wind_degrees)
        self.daytime_wind_speed_avg_kmh = data.get('daytimeForecast', {}).get('windSpeed')
        self.daytime_wind_speed_avg_mph = self.kmh_to_mph(self.daytime_wind_speed_avg_kmh)

        self.overnight_cloud_cover = data.get('overnightForecast', {}).get('cloudCover')
        self.overnight_condition_code = data.get('overnightForecast', {}).get('conditionCode')
        self.overnight_conditions = self.conditions_for_code(self.overnight_condition_code)
        self.overnight_icon = self.icon_for_condition_code(self.overnight_condition_code)
        self.overnight_humidity = data.get('overnightForecast', {}).get('humidity')
        self.overnight_precip_amount_mm = data.get('overnightForecast', {}).get('precipitationAmount')
        self.overnight_precip_amount_in = self.millimeters_to_inches(self.overnight_precip_amount_mm)
        self.overnight_precip_chance = data.get('overnightForecast', {}).get('precipitationChance')
        self.overnight_precip_type = data.get('overnightForecast', {}).get('precipitationType')
        self.overnight_snowfall_amount_mm = data.get('overnightForecast', {}).get('snowfallAmount')
        self.overnight_snowfall_amount_in = self.millimeters_to_inches(self.overnight_snowfall_amount_mm)
        self.overnight_wind_degrees = data.get('overnightForecast', {}).get('windDirection')
        self.overnight_wind_direction = self.degrees_to_cardinal(self.overnight_wind_degrees)
        self.overnight_wind_speed_avg_kmh = data.get('overnightForecast', {}).get('windSpeed')
        self.overnight_wind_speed_avg_mph = self.kmh_to_mph(self.overnight_wind_speed_avg_kmh)

        self.nighttime_cloud_cover = data.get('restOfDayForecast', {}).get('cloudCover')
        self.nighttime_condition_code = data.get('restOfDayForecast', {}).get('conditionCode')
        self.nighttime_conditions = self.conditions_for_code(self.nighttime_condition_code)
        self.nighttime_icon = self.icon_for_condition_code(self.nighttime_condition_code)
        self.nighttime_humidity = data.get('restOfDayForecast', {}).get('humidity')
        self.nighttime_precip_amount_mm = data.get('restOfDayForecast', {}).get('precipitationAmount')
        self.nighttime_precip_amount_in = self.millimeters_to_inches(self.nighttime_precip_amount_mm)
        self.nighttime_precip_chance = data.get('restOfDayForecast', {}).get('precipitationChance')
        self.nighttime_precip_type = data.get('restOfDayForecast', {}).get('precipitationType')
        self.nighttime_snowfall_amount_mm = data.get('restOfDayForecast', {}).get('snowfallAmount')
        self.nighttime_snowfall_amount_in = self.millimeters_to_inches(self.nighttime_snowfall_amount_mm)
        self.nighttime_wind_degrees = data.get('restOfDayForecast', {}).get('windDirection')
        self.nighttime_wind_direction = self.degrees_to_cardinal(self.nighttime_wind_degrees)
        self.nighttime_wind_speed_avg_kmh = data.get('restOfDayForecast', {}).get('windSpeed')
        self.nighttime_wind_speed_avg_mph = self.kmh_to_mph(self.nighttime_wind_speed_avg_kmh)


class WeatherKitResponse():

    def __init__(self):
        self.current_weather = None
        self.forecast_next_hour = None
        self.forecast_hourly = None
        self.forecast_daily = None

    def as_json(self):
        return jsonpickle.encode(self)
