from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import forecast
from .models import UserLocation
from django.contrib.auth.models import User
import json

# Create your views here.

class WeatherView(APIView):
    def get(self, request, format=None):
        search = json.dumps(request.GET)
        search = json.loads(search)
        data = forecast.location(search)
        weather_raw = data['weather']
        current = data['current']
        address = data['address']
        weather = WeatherView.transform_weather_data(weather_raw)
        supplement_data = data['supplement']
        transformed_supplement = {}
        if supplement_data:
            for date, forecasts in supplement_data['supplement'].items():
                detailed_forecasts = [{'detailedForecast': period['detailedForecast'], 
                                    'isDaytime': period['isDaytime']} for period in forecasts]
                transformed_supplement[date] = detailed_forecasts
                supplement = transformed_supplement
        else:
            supplement_data = {}
            for date in weather_raw['date']:
                supplement_data[date] = ["No supplemental data available for this location."]
            supplement = supplement_data
        geodata = data['geodata']
        country_code = search['country_code']
        timezone = search['timezone']
        # 

        result = { 'weather': weather, 
                    'address': address, 
                    'supplemental': supplement, 
                    'geodata': geodata,
                    'current': current,
                    'country_code': country_code,
                    'timezone': timezone
                    }

        return Response(result)
    
    
    
    def post(self, request, format=None):
        user_id = request.data['user']
        user = User.objects.get(id=user_id)
        address = request.data['address']
        nickname = request.data['nickname']
        lat = request.data['lat']
        lon = request.data['lon']
        timezone = request.data['timezone']
        country_code = request.data['country_code']
        user_location = UserLocation(user=user, address=address, nickname=nickname, lat=lat, lon=lon, timezone=timezone, country_code=country_code)
        user_location.save()
        return Response({'status': 'success'})
    
    @staticmethod
    def transform_weather_data(weather_data):
        transformed_data = []
        for i in range(len(weather_data['date'])):  
            day_data = {}
            for key, values in weather_data.items():
                day_data[key] = values[i]  
            transformed_data.append(day_data)
        return transformed_data
    
class UserLocationView(APIView):
    def get(self, request, format=None):
        user_id = request.GET['user']
        user = User.objects.get(id=user_id)
        user_locations = UserLocation.objects.filter(user=user)
        locations = []
        for location in user_locations:
            locations.append({
                'locationId': location.id,
                'address': location.address,
                'nickname': location.nickname,
                'lat': location.lat,
                'lon': location.lon,
                'formatted': location.address,
                'timezone': location.timezone,
                'country_code': location.country_code
            })
        return Response(locations)
    
    def delete(self, request, format=None):
        location_id = request.data['location_id']
        location = UserLocation.objects.get(id=location_id)
        user = location.user
        location.delete()
        user_locations = UserLocation.objects.filter(user=user)
        locations = []
        for location in user_locations:
            locations.append({
                'locationId': location.id,
                'address': location.address,
                'nickname': location.nickname,
                'lat': location.lat,
                'lon': location.lon
            })
    
        return Response({'status': 'success', 'data': locations})
    
    def put(self, request, format=None):
        location_id = request.data['location_id']
        nickname = request.data['nickname']
        location = UserLocation.objects.get(id=location_id)
        location.nickname = nickname
        location.save()
        return Response({'status': 'success'})