#!/usr/bin/env python3
"""
Test final pentru integrarea weather în CarpatiNest
Verifică toate componentele weather: API, JavaScript, CSS și template
"""

import requests
import json
from pathlib import Path

def test_weather_api():
    """Testează API-urile weather"""
    print("🌤️  Testing Weather API Integration")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test current weather API
    print("1. Testing current weather API...")
    try:
        response = requests.get(f"{base_url}/api/weather/105/")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("   ✅ Current weather API: SUCCESS")
                print(f"   📍 Location: {data.get('refuge_name')}")
                weather = data.get('current_weather', {})
                print(f"   🌡️  Temperature: {weather.get('temperature')}°C")
                print(f"   ☁️  Condition: {weather.get('description')}")
            else:
                print("   ❌ Current weather API returned error")
        else:
            print(f"   ❌ Current weather API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Current weather API error: {e}")
    
    # Test forecast API
    print("\n2. Testing forecast API...")
    try:
        response = requests.get(f"{base_url}/api/weather/105/forecast/?date=2025-06-07")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("   ✅ Forecast API: SUCCESS")
                weather = data.get('weather', {})
                print(f"   📅 Date: {data.get('date')}")
                print(f"   🌡️  Temperature: {weather.get('min_temp')}°C - {weather.get('max_temp')}°C")
                print(f"   ☁️  Condition: {weather.get('description')}")
                rec = data.get('recommendation', {})
                print(f"   🥾 Hiking suitable: {data.get('hiking_suitable')}")
                print(f"   💡 Recommendation: {rec.get('message', 'N/A')}")
            else:
                print("   ❌ Forecast API returned error")
        else:
            print(f"   ❌ Forecast API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Forecast API error: {e}")

def test_static_files():
    """Verifică fișierele statice"""
    print("\n3. Testing static files...")
    
    static_dir = Path("CarpatiNest_app/static")
    
    # Check CSS
    weather_css = static_dir / "css" / "weather.css"
    if weather_css.exists():
        print("   ✅ weather.css: EXISTS")
    else:
        print("   ❌ weather.css: MISSING")
    
    # Check JavaScript
    weather_js = static_dir / "js" / "weather.js"
    if weather_js.exists():
        print("   ✅ weather.js: EXISTS")
    else:
        print("   ❌ weather.js: MISSING")
    
    flatpickr_js = static_dir / "js" / "flatpickr-init.js"
    if flatpickr_js.exists():
        print("   ✅ flatpickr-init.js: EXISTS")
    else:
        print("   ❌ flatpickr-init.js: MISSING")

def test_template_integration():
    """Verifică integrarea în template"""
    print("\n4. Testing template integration...")
    
    booking_template = Path("CarpatiNest_app/templates/booking.html")
    if booking_template.exists():
        content = booking_template.read_text(encoding='utf-8')
        
        # Check for weather CSS
        if 'weather.css' in content:
            print("   ✅ weather.css included in template")
        else:
            print("   ❌ weather.css NOT included in template")
        
        # Check for weather JavaScript
        if 'weather.js' in content:
            print("   ✅ weather.js included in template")
        else:
            print("   ❌ weather.js NOT included in template")
        
        # Check for weather sections
        if 'weather-section' in content:
            print("   ✅ Weather section present in template")
        else:
            print("   ❌ Weather section NOT found in template")
        
        # Check for weather service initialization
        if 'WeatherService' in content:
            print("   ✅ WeatherService initialization found")
        else:
            print("   ❌ WeatherService initialization NOT found")
    else:
        print("   ❌ booking.html template NOT found")

def test_booking_page():
    """Testează pagina de booking"""
    print("\n5. Testing booking page...")
    try:
        response = requests.get("http://127.0.0.1:8000/booking/105/")
        if response.status_code == 200:
            print("   ✅ Booking page accessible")
            if 'weather-section' in response.text:
                print("   ✅ Weather section rendered in page")
            else:
                print("   ❌ Weather section NOT found in rendered page")
        else:
            print(f"   ❌ Booking page failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Booking page error: {e}")

def main():
    """Rulează toate testele"""
    print("🏔️  CarpatiNest Weather Integration - Final Test")
    print("=" * 60)
    
    test_weather_api()
    test_static_files()
    test_template_integration()
    test_booking_page()
    
    print("\n" + "=" * 60)
    print("🎯 Test completed! Check results above.")
    print("\n📋 Summary:")
    print("   • Weather APIs should return real data from OpenWeatherMap")
    print("   • Static files (CSS/JS) should be present")
    print("   • Template should include weather integration")
    print("   • Booking page should display weather section")
    print("\n🚀 If all tests pass, weather integration is complete!")

if __name__ == "__main__":
    main()
