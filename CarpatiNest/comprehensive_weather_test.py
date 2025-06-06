#!/usr/bin/env python
"""
Comprehensive test for weather integration functionality
Tests both backend APIs and frontend JavaScript integration
"""

import json
import requests
import time
from datetime import datetime, timedelta

def test_weather_apis():
    """Test weather API endpoints"""
    base_url = "http://127.0.0.1:8000"
    refuge_id = 105
    
    print("🌤️  Testing Weather Integration - Comprehensive Test")
    print("=" * 60)
    
    # Test current weather API
    print("\n1. Testing Current Weather API...")
    try:
        response = requests.get(f"{base_url}/api/weather/{refuge_id}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Current Weather API: SUCCESS")
            print(f"   📍 Location: {data.get('location', 'N/A')}")
            print(f"   🌡️  Temperature: {data.get('temperature', 'N/A')}°C")
            print(f"   📝 Description: {data.get('description', 'N/A')}")
            print(f"   💨 Wind Speed: {data.get('wind_speed', 'N/A')} m/s")
            print(f"   💧 Humidity: {data.get('humidity', 'N/A')}%")
        else:
            print(f"   ❌ Current Weather API failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Current Weather API error: {e}")
    
    # Test forecast API
    print("\n2. Testing Weather Forecast API...")
    try:
        response = requests.get(f"{base_url}/api/weather/{refuge_id}/forecast/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Forecast API: SUCCESS")
            print(f"   📊 Forecast days: {len(data.get('forecasts', []))}")
            
            # Show first 2 days
            forecasts = data.get('forecasts', [])
            for i, forecast in enumerate(forecasts[:2]):
                print(f"   📅 Day {i+1}: {forecast.get('date')} - {forecast.get('temperature')}°C - {forecast.get('description')}")
        else:
            print(f"   ❌ Forecast API failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Forecast API error: {e}")
    
    # Test specific date forecast
    print("\n3. Testing Specific Date Forecast API...")
    try:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        response = requests.get(f"{base_url}/api/weather/{refuge_id}/forecast/{tomorrow}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Date-specific Forecast API: SUCCESS")
            print(f"   📅 Date: {data.get('date')}")
            print(f"   🌡️  Temperature: {data.get('temperature')}°C")
            print(f"   📝 Description: {data.get('description')}")
            print(f"   🎯 Recommendation: {data.get('recommendation', 'N/A')}")
        else:
            print(f"   ❌ Date-specific Forecast API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Date-specific Forecast API error: {e}")
    
    # Test booking page accessibility
    print("\n4. Testing Booking Page Accessibility...")
    try:
        response = requests.get(f"{base_url}/booking/{refuge_id}/")
        if response.status_code == 200:
            print(f"   ✅ Booking Page: SUCCESS")
            print(f"   📄 Page loaded successfully")
            
            # Check for weather-related content
            content = response.text
            weather_checks = [
                ('weather.css', 'Weather CSS included'),
                ('weather.js', 'Weather JS included'),
                ('weather-container', 'Weather container present'),
                ('forecast-container', 'Forecast container present'),
                ('WeatherService', 'WeatherService initialization present')
            ]
            
            for check, description in weather_checks:
                if check in content:
                    print(f"   ✅ {description}")
                else:
                    print(f"   ❌ {description} - NOT FOUND")
        else:
            print(f"   ❌ Booking Page failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Booking Page error: {e}")
    
    # Test static files
    print("\n5. Testing Static Files...")
    static_files = [
        ('/static/js/weather.js', 'Weather JavaScript'),
        ('/static/css/weather.css', 'Weather CSS')
    ]
    
    for path, description in static_files:
        try:
            response = requests.get(f"{base_url}{path}")
            if response.status_code == 200:
                print(f"   ✅ {description}: SUCCESS")
                print(f"   📦 File size: {len(response.content)} bytes")
            else:
                print(f"   ❌ {description} failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {description} error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Weather Integration Test Complete!")
    print("\nNext Steps:")
    print("1. Open http://127.0.0.1:8000/booking/105/ in browser")
    print("2. Check browser console for JavaScript errors")
    print("3. Verify weather widget displays correctly")
    print("4. Test date selection to see weather recommendations")

if __name__ == "__main__":
    test_weather_apis()
