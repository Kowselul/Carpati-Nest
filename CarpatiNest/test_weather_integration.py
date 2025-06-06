#!/usr/bin/env python
"""
Script de test pentru integrarea API-ului de vreme
Testează funcționalitatea weather service fără a necesita o cheie API reală
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarpatiNest.settings')
django.setup()

from CarpatiNest_app.models import Refuge
from CarpatiNest_app.weather_service import WeatherService

def test_weather_service_mock():
    """Test cu date mock pentru weather service"""
    print("🌤️  Testare Weather Service - CarpatiNest")
    print("=" * 50)
    
    # Găsește primul refugiu cu coordonate GPS
    refuge = Refuge.objects.filter(
        latitude__isnull=False, 
        longitude__isnull=False
    ).first()
    
    if not refuge:
        print("❌ Nu s-au găsit refugii cu coordonate GPS!")
        return
    
    print(f"📍 Testare vreme pentru: {refuge.name}")
    print(f"   Coordonate: {refuge.latitude}, {refuge.longitude}")
    print()
    
    # Testare weather service
    weather_service = WeatherService()
    
    # Verifică configurația API key
    if not weather_service.api_key or weather_service.api_key == 'demo-key-get-from-openweathermap':
        print("⚠️  API Key nu este configurat - funcționând în modul demo")
        print("   Pentru funcționalitate completă, obține o cheie gratuită de la:")
        print("   https://openweathermap.org/api")
        print()
        
        # Creează date mock pentru demonstrație
        mock_weather = {
            'temperature': 15,
            'feels_like': 12,
            'humidity': 65,
            'pressure': 1013,
            'description': 'Parțial înnorat',
            'icon': '02d',
            'wind_speed': 5.2,
            'wind_direction': 180,
            'visibility': 10.0,
            'clouds': 30,
            'location': f"Zona {refuge.name}"
        }
        
        print("🌡️  Date meteo mock pentru demonstrație:")
        print(f"   Temperatură: {mock_weather['temperature']}°C")
        print(f"   Se simte ca: {mock_weather['feels_like']}°C")
        print(f"   Descriere: {mock_weather['description']}")
        print(f"   Umiditate: {mock_weather['humidity']}%")
        print(f"   Vânt: {mock_weather['wind_speed']} m/s")
        print(f"   Vizibilitate: {mock_weather['visibility']} km")
        print()
        
        # Testare recomandare drumeție
        recommendation = weather_service.get_hiking_recommendation(mock_weather)
        print("🥾 Recomandare drumeție:")
        print(f"   Potrivit: {'✅ Da' if recommendation['suitable'] else '❌ Nu'}")
        print(f"   Nivel: {recommendation['level']}")
        print(f"   Mesaj: {recommendation['message']}")
        print()
        
    else:
        print("🔑 API Key configurat - testare cu date reale...")
        
        # Încearcă să obțină date reale
        current_weather = weather_service.get_current_weather(
            refuge.latitude, 
            refuge.longitude
        )
        
        if current_weather:
            print("✅ Date meteo obținute cu succes!")
            print(f"   Temperatură: {current_weather['temperature']}°C")
            print(f"   Descriere: {current_weather['description']}")
            print(f"   Umiditate: {current_weather['humidity']}%")
            print(f"   Vânt: {current_weather['wind_speed']} m/s")
            print()
            
            # Testare recomandare
            recommendation = weather_service.get_hiking_recommendation(current_weather)
            print("🥾 Recomandare drumeție:")
            print(f"   Potrivit: {'✅ Da' if recommendation['suitable'] else '❌ Nu'}")
            print(f"   Mesaj: {recommendation['message']}")
            print()
        else:
            print("❌ Nu s-au putut obține datele meteo")
            print("   Verifică conexiunea la internet și cheia API")
    
    print("🔗 URL-uri API disponibile:")
    print(f"   Vreme curentă: /api/weather/{refuge.id}/")
    print(f"   Prognoză: /api/weather/{refuge.id}/forecast/")
    print()
    
    print("📋 Frontend:")
    print("   - CSS: /static/css/weather.css")
    print("   - JavaScript: /static/js/weather.js") 
    print("   - Integrat în: booking.html")
    print()
    
    print("✅ Test completat!")

def test_gps_coordinates():
    """Testează coordonatele GPS ale refugiilor"""
    print("\n📍 Verificare coordonate GPS")
    print("=" * 30)
    
    total_refuges = Refuge.objects.count()
    refuges_with_gps = Refuge.objects.filter(
        latitude__isnull=False, 
        longitude__isnull=False
    ).count()
    
    print(f"Total refugii: {total_refuges}")
    print(f"Cu coordonate GPS: {refuges_with_gps}")
    print(f"Fără coordonate: {total_refuges - refuges_with_gps}")
    
    if refuges_with_gps > 0:
        print("\n📍 Refugii cu coordonate GPS:")
        for refuge in Refuge.objects.filter(latitude__isnull=False, longitude__isnull=False)[:5]:
            print(f"   {refuge.name}: {refuge.latitude}, {refuge.longitude}")
        if refuges_with_gps > 5:
            print(f"   ... și încă {refuges_with_gps - 5} refugii")

if __name__ == "__main__":
    test_gps_coordinates()
    test_weather_service_mock()
