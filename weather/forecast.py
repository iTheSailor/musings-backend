import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import requests
from requests.structures import CaseInsensitiveDict
import os
import time
import json

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def location(result):
	lon = result['lon']
	lat = result['lat']
	timezone = result['timezone']
	_address = result['formatted']
	country_code = result['country_code']
	geodata= {
		"lat": lat,
		"lon": lon
	}
	supplement = None
	if country_code == "us":
		location = (lat, lon)
		supplement = supplemental(location)
	location = (lat, lon, timezone)

	weather = forecast(location)[0]
	current = forecast(location)[1]
	data = {"address": _address, "weather": weather, "supplement": supplement, "geodata": geodata, "current": current}
	return data

def supplemental(search):
	lat = search[0]
	long = search[1]
	url = f'https://api.weather.gov/points/{lat},{long}'
	get_weather = requests.get(f'https://api.weather.gov/points/{lat},{long}')
	print(url)
	time.sleep(1)
	weather_json = get_weather.json()
	forecast_url = weather_json['properties']['forecast']
	print(forecast_url)
	forecast = requests.get(forecast_url).json()
	forecast = forecast['properties']['periods']
	weather_by_date = {}
	for period in forecast:
		date_str = period['startTime'].split('T')[0]
		if date_str not in weather_by_date:
			weather_by_date[date_str] = []
		weather_by_date[date_str].append(period)

	weather_bundle = {
		'supplement': weather_by_date,
	}


	return weather_bundle


def forecast(search):
	lattitude = search[0]
	longitude = search[1]
	timezone = search[2]
	params={
		"latitude": lattitude,
		"longitude": longitude,
		"current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "cloud_cover", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "weather_code","is_day"],
		"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "precipitation_sum", "precipitation_hours", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max"],
		"forecast_hours": 6,
		"temperature_unit": "fahrenheit",
		"wind_speed_unit": "mph",
		"precipitation_unit": "inch",
		"timezone": timezone,
	}
	url = "https://api.open-meteo.com/v1/forecast"	
	responses = openmeteo.weather_api(url, params=params)
	response = responses[0]

	current = response.Current()
	current_temperature_2m = current.Variables(0).Value()
	current_relative_humidity_2m = current.Variables(1).Value()
	current_apparent_temperature = current.Variables(2).Value()
	current_precipitation = current.Variables(3).Value()
	current_cloud_cover = current.Variables(4).Value()
	current_wind_speed_10m = current.Variables(5).Value()
	current_wind_direction_10m = current.Variables(6).Value()
	current_wind_gusts_10m = current.Variables(7).Value()
	current_weather_code = current.Variables(8).Value()
	current_is_day = current.Variables(9).Value()
	# Assuming 'current' is a proper response object containing the current weather data
	current_dict = {}

	current_dict["temperature"] = current_temperature_2m
	current_dict["relative_humidity"] = current_relative_humidity_2m
	current_dict["feelsLike"] = current_apparent_temperature
	current_dict["precipitation"] = current_precipitation
	current_dict["cloud_cover"] = current_cloud_cover
	current_dict["wind_speed"] = current_wind_speed_10m
	current_dict["wind_direction"] = current_wind_direction_10m
	current_dict["wind_gusts"] = current_wind_gusts_10m
	current_dict["code"] = str(int(current_weather_code))
	if current_is_day == 1:
		current_dict["is_day"] = "day"
	else:
		current_dict["is_day"] = "night"

	daily = response.Daily()
	daily_weather_code = daily.Variables(0).ValuesAsNumpy()
	daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
	daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
	daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
	daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
	daily_precipitation_sum = daily.Variables(5).ValuesAsNumpy()
	daily_precipitation_hours = daily.Variables(6).ValuesAsNumpy()
	daily_precipitation_probability_max = daily.Variables(7).ValuesAsNumpy()
	daily_wind_speed_10m_max = daily.Variables(8).ValuesAsNumpy()
	daily_wind_gusts_10m_max = daily.Variables(9).ValuesAsNumpy()
	daily_data = {"date": pd.date_range(
		start = pd.to_datetime(daily.Time(), unit = "s"),
		end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	)}
	daily_data["weather_code"] = daily_weather_code
	daily_data["temperature_2m_max"] = daily_temperature_2m_max
	daily_data["temperature_2m_min"] = daily_temperature_2m_min
	daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
	daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
	daily_data["precipitation_sum"] = daily_precipitation_sum
	daily_data["precipitation_hours"] = daily_precipitation_hours
	daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
	daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
	daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max


	daily_dataframe = pd.DataFrame(data = daily_data)
	daily_dict = daily_dataframe.to_dict()

	# print(daily_dataframe, hourly_dataframe)

	return daily_dict, current_dict