import requests
from django.conf import settings
from decouple import config
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Serviciu pentru obținerea datelor meteo de la OpenWeatherMap API
    """
    
    def __init__(self):
        self.api_key = config('WEATHER_API_KEY', default='')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
    def get_current_weather(self, latitude, longitude):
        """
        Obține vremea curentă pentru coordonatele date
        """
        if not self.api_key:
            logger.warning("Weather API key not configured")
            return None
            
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric',  # Pentru temperaturi în Celsius
                'lang': 'ro'        # Pentru descrieri în română
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._format_current_weather(data)
            
        except requests.RequestException as e:
            logger.error(f"Error fetching current weather: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in weather service: {e}")
            return None
    
    def get_weather_forecast(self, latitude, longitude, days=5):
        """
        Obține prognoza meteo pentru următoarele zile
        """
        if not self.api_key:
            logger.warning("Weather API key not configured")
            return None
            
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'ro',
                'cnt': days * 8  # 8 predicții pe zi (la 3 ore)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._format_forecast(data)
            
        except requests.RequestException as e:
            logger.error(f"Error fetching weather forecast: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in forecast service: {e}")
            return None
    
    def _format_current_weather(self, data):
        """
        Formatează datele meteo curente într-un format standardizat
        """
        try:
            return {
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                'clouds': data['clouds']['all'],
                'timestamp': datetime.now(),
                'location': f"{data['name']}, {data['sys']['country']}"
            }
        except KeyError as e:
            logger.error(f"Error formatting weather data: {e}")
            return None
    
    def _format_forecast(self, data):
        """
        Formatează datele prognozei meteo
        """
        try:
            forecast_list = []
            city_info = {
                'name': data['city']['name'],
                'country': data['city']['country'],
                'sunrise': datetime.fromtimestamp(data['city']['sunrise']),
                'sunset': datetime.fromtimestamp(data['city']['sunset'])
            }
            
            for item in data['list']:
                forecast_item = {
                    'datetime': datetime.fromtimestamp(item['dt']),
                    'temperature': round(item['main']['temp']),
                    'temperature_min': round(item['main']['temp_min']),
                    'temperature_max': round(item['main']['temp_max']),
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'].capitalize(),
                    'icon': item['weather'][0]['icon'],
                    'wind_speed': item['wind']['speed'],
                    'clouds': item['clouds']['all'],
                    'precipitation_probability': item.get('pop', 0) * 100  # Convert to percentage
                }
                forecast_list.append(forecast_item)
            
            return {
                'city': city_info,
                'forecast': forecast_list
            }
        except KeyError as e:
            logger.error(f"Error formatting forecast data: {e}")
            return None
    
    def get_weather_alerts(self, latitude, longitude):
        """
        Obține alertele meteo pentru coordonatele date
        """
        if not self.api_key:
            return None
            
        try:
            url = f"{self.base_url}/onecall"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'exclude': 'minutely,hourly,daily',
                'lang': 'ro'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            alerts = data.get('alerts', [])
            
            formatted_alerts = []
            for alert in alerts:
                formatted_alert = {
                    'event': alert['event'],
                    'description': alert['description'],
                    'start': datetime.fromtimestamp(alert['start']),
                    'end': datetime.fromtimestamp(alert['end']),
                    'sender_name': alert['sender_name']
                }
                formatted_alerts.append(formatted_alert)
            
            return formatted_alerts
            
        except requests.RequestException as e:
            logger.error(f"Error fetching weather alerts: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in alerts service: {e}")
            return []
    
    def is_good_hiking_weather(self, weather_data):
        """
        Determină dacă vremea este bună pentru drumeții
        """
        if not weather_data:
            return False
            
        temp = weather_data['temperature']
        wind_speed = weather_data['wind_speed']
        humidity = weather_data['humidity']
        description = weather_data['description'].lower()
        
        # Criterii pentru vreme bună de drumeție
        good_temp = -5 <= temp <= 25  # Temperatură acceptabilă
        low_wind = wind_speed < 10    # Vânt nu prea puternic
        no_bad_weather = not any(word in description for word in 
                               ['ploaie', 'torentiala', 'ninsoare', 'ceata', 'furtuna'])
        
        return good_temp and low_wind and no_bad_weather
    
    def get_hiking_recommendation(self, weather_data):
        """
        Oferă o recomandare pentru drumeție bazată pe vremea curentă
        """
        if not weather_data:
            return {
                'suitable': False,
                'message': "Datele meteo nu sunt disponibile",
                'level': 'unknown'
            }
        
        temp = weather_data['temperature']
        wind_speed = weather_data['wind_speed']
        description = weather_data['description'].lower()
        
        # Analiza detaliată
        if any(word in description for word in ['furtuna', 'torentiala']):
            return {
                'suitable': False,
                'message': "Condiții meteorologice periculoase. Se recomandă amânarea drumeției.",
                'level': 'dangerous'
            }
        elif temp < -10 or temp > 30:
            return {
                'suitable': False,
                'message': f"Temperatură extremă ({temp}°C). Condiții dificile pentru drumeție.",
                'level': 'difficult'
            }
        elif wind_speed > 15:
            return {
                'suitable': False,
                'message': f"Vânt puternic ({wind_speed} m/s). Drumeția poate fi periculoasă.",
                'level': 'risky'
            }
        elif self.is_good_hiking_weather(weather_data):
            return {
                'suitable': True,
                'message': "Condiții excelente pentru drumeție! Bucurați-vă de natură.",
                'level': 'excellent'
            }
        else:
            return {
                'suitable': True,
                'message': "Condiții acceptabile pentru drumeție. Luați echipament adecvat.",
                'level': 'acceptable'
            }

# Instanță globală a serviciului
weather_service = WeatherService()
