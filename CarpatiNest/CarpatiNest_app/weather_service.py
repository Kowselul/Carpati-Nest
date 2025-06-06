try:
    import requests
except ImportError:
    requests = None
    
from django.conf import settings
from datetime import datetime, timedelta
import logging

# Try to import decouple, if it fails use default values
try:
    from decouple import config
except ImportError:
    # Fallback function if decouple is not available
    def config(key, default=None, cast=None):
        import os
        value = os.environ.get(key, default)
        if cast and value:
            return cast(value)
        return value

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Serviciu pentru obținerea datelor meteo de la OpenWeatherMap API
    """
    
    def __init__(self):
        if not requests:
            logger.error("requests library is not available. Weather functionality will be disabled.")
            self.api_key = None
            return
            
        self.api_key = config('OPENWEATHER_API_KEY', default='')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
    def get_current_weather(self, latitude, longitude):
        """
        Obține vremea curentă pentru coordonatele date
        """
        if not requests:
            logger.error("requests library is not available")
            return None
            
        if not self.api_key:
            logger.warning("Weather API key not configured")
            return None
            
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'ro'
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
            
    def get_forecast(self, latitude, longitude, days=5):
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
        if not data:
            return None
            
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
                'visibility': data.get('visibility', 0) / 1000,  # convertit în km
                'location': data['name'],
                'timestamp': datetime.now().isoformat()
            }
        except (KeyError, TypeError) as e:
            logger.error(f"Error formatting current weather data: {e}")
            return None
    
    def _format_forecast(self, data):
        """
        Formatează datele prognozei meteo
        """
        if not data or 'list' not in data:
            return None
            
        try:
            forecast_list = []
            daily_data = {}
            
            for item in data['list']:
                dt = datetime.fromtimestamp(item['dt'])
                date_key = dt.date()
                
                if date_key not in daily_data:
                    daily_data[date_key] = {
                        'date': date_key.isoformat(),
                        'temperatures': [],
                        'humidity': [],
                        'descriptions': [],
                        'icons': [],
                        'wind_speeds': []
                    }
                
                daily_data[date_key]['temperatures'].append(item['main']['temp'])
                daily_data[date_key]['humidity'].append(item['main']['humidity'])
                daily_data[date_key]['descriptions'].append(item['weather'][0]['description'])
                daily_data[date_key]['icons'].append(item['weather'][0]['icon'])
                daily_data[date_key]['wind_speeds'].append(item['wind']['speed'])
            
            # Creează prognoza zilnică
            for date_key, day_data in sorted(daily_data.items()):
                forecast_list.append({
                    'date': day_data['date'],
                    'min_temp': round(min(day_data['temperatures'])),
                    'max_temp': round(max(day_data['temperatures'])),
                    'avg_humidity': round(sum(day_data['humidity']) / len(day_data['humidity'])),
                    'description': max(set(day_data['descriptions']), key=day_data['descriptions'].count),
                    'icon': max(set(day_data['icons']), key=day_data['icons'].count),
                    'avg_wind_speed': round(sum(day_data['wind_speeds']) / len(day_data['wind_speeds']), 1)
                })
            
            return forecast_list[:5]  # returnează doar primele 5 zile
            
        except (KeyError, TypeError, ValueError) as e:
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
                'exclude': 'minutely,hourly,daily'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('alerts', [])
                
        except requests.RequestException as e:
            logger.error(f"Error fetching weather alerts: {e}")
            
        return []
    
    def is_good_hiking_weather(self, weather_data):
        """
        Determină dacă vremea este bună pentru drumeții
        """
        if not weather_data:
            return False
            
        temp = weather_data.get('temperature', 0)
        wind_speed = weather_data.get('wind_speed', 0)
        description = weather_data.get('description', '').lower()
        
        # Criterii pentru vremea bună
        good_temp = -5 <= temp <= 35  # Temperaturi rezonabile
        low_wind = wind_speed < 10  # Vânt moderat
        no_bad_weather = not any(bad in description for bad in ['ploaie', 'ninsoare', 'furtună', 'ceață'])
        
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
        
        temp = weather_data.get('temperature', 0)
        wind_speed = weather_data.get('wind_speed', 0)
        description = weather_data.get('description', '').lower()
        humidity = weather_data.get('humidity', 0)
        
        # Analiză detaliată
        if temp < -10:
            return {
                'suitable': False,
                'message': "Temperaturile foarte scăzute fac drumeția periculoasă. Recomandăm să amânați excursia.",
                'level': 'danger'
            }
        elif temp > 35:
            return {
                'suitable': False,
                'message': "Temperaturile foarte ridicate pot fi periculoase. Evitați drumeția în timpul zilei.",
                'level': 'danger'
            }
        elif wind_speed > 15:
            return {
                'suitable': False,
                'message': "Vântul puternic face drumeția dificilă și potențial periculoasă.",
                'level': 'danger'
            }
        elif any(bad in description for bad in ['furtună', 'lightning']):
            return {
                'suitable': False,
                'message': "Condițiile meteo severe fac drumeția extrem de periculoasă.",
                'level': 'danger'
            }
        elif any(bad in description for bad in ['ploaie', 'rain']):
            return {
                'suitable': False,
                'message': "Ploaia face cărările alunecoase și drumeția mai periculoasă.",
                'level': 'warning'
            }
        elif any(bad in description for bad in ['ninsoare', 'snow']):
            return {
                'suitable': False,
                'message': "Ninsoarea poate face cărările impracticabile. Echipament de iarnă necesar.",
                'level': 'warning'
            }
        elif temp < 0:
            return {
                'suitable': True,
                'message': "Vremea este rece dar acceptabilă pentru drumeție. Echipament de iarnă recomandat.",
                'level': 'caution'
            }
        elif wind_speed > 10:
            return {
                'suitable': True,
                'message': "Vântul moderat. Îmbrăcați-vă corespunzător și fiți atenți.",
                'level': 'caution'
            }
        elif humidity > 80:
            return {
                'suitable': True,
                'message': "Umiditate ridicată. Hidratați-vă des și luați pauze regulate.",
                'level': 'caution'
            }
        else:
            return {
                'suitable': True,
                'message': "Condițiile meteo sunt excelente pentru drumeție! Bucurați-vă de natură.",
                'level': 'excellent'
            }
