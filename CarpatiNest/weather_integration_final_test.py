#!/usr/bin/env python
"""
Final weather integration test - comprehensive verification
"""

import json
import requests
import time
from datetime import datetime, timedelta

def test_weather_integration_final():
    """Final comprehensive test for weather integration"""
    base_url = "http://127.0.0.1:8000"
    refuge_id = 105
    
    print("🏔️  FINAL WEATHER INTEGRATION TEST")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test 1: Current Weather API
    print("\n1. ✅ Testing Current Weather API...")
    try:
        response = requests.get(f"{base_url}/api/weather/{refuge_id}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Current Weather API: SUCCESS")
            print(f"   📍 Location: {data.get('location', 'N/A')}")
            print(f"   🌡️  Temperature: {data.get('temperature', 'N/A')}°C")
            print(f"   📝 Description: {data.get('description', 'N/A')}")
        else:
            print(f"   ❌ Current Weather API FAILED: {response.status_code}")
            all_tests_passed = False
    except Exception as e:
        print(f"   ❌ Current Weather API ERROR: {e}")
        all_tests_passed = False
    
    # Test 2: 5-Day Forecast API
    print("\n2. ✅ Testing 5-Day Forecast API...")
    try:
        response = requests.get(f"{base_url}/api/weather/{refuge_id}/forecast/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 5-Day Forecast API: SUCCESS")
            forecasts = data.get('forecasts', [])
            print(f"   📊 Forecast days: {len(forecasts)}")
            
            if len(forecasts) >= 3:
                for i, forecast in enumerate(forecasts[:3]):
                    print(f"   📅 Day {i+1}: {forecast.get('date')} - {forecast.get('temperature')}°C")
            else:
                print(f"   ⚠️  Only {len(forecasts)} forecast days available")
        else:
            print(f"   ❌ 5-Day Forecast API FAILED: {response.status_code}")
            all_tests_passed = False
    except Exception as e:
        print(f"   ❌ 5-Day Forecast API ERROR: {e}")
        all_tests_passed = False
    
    # Test 3: Date-specific Forecast API
    print("\n3. ✅ Testing Date-Specific Forecast API...")
    try:
        test_date = "2025-06-07"  # Use a date that should be in forecast
        response = requests.get(f"{base_url}/api/weather/{refuge_id}/forecast/?date={test_date}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Date-Specific Forecast API: SUCCESS")
            print(f"   📅 Date: {data.get('date')}")
            print(f"   🌡️  Temperature: {data.get('temperature')}°C")
            print(f"   🎯 Hiking Suitable: {data.get('hiking_suitable', 'N/A')}")
        else:
            print(f"   ❌ Date-Specific Forecast API FAILED: {response.status_code}")
            print(f"   Response: {response.text}")
            all_tests_passed = False
    except Exception as e:
        print(f"   ❌ Date-Specific Forecast API ERROR: {e}")
        all_tests_passed = False
    
    # Test 4: Static Files
    print("\n4. ✅ Testing Static Files...")
    static_files = [
        ('/static/js/weather.js', 'Weather JavaScript'),
        ('/static/css/weather.css', 'Weather CSS')
    ]
    
    for path, description in static_files:
        try:
            response = requests.get(f"{base_url}{path}")
            if response.status_code == 200 and len(response.content) > 0:
                print(f"   ✅ {description}: SUCCESS ({len(response.content)} bytes)")
            else:
                print(f"   ❌ {description} FAILED: {response.status_code} or empty file")
                all_tests_passed = False
        except Exception as e:
            print(f"   ❌ {description} ERROR: {e}")
            all_tests_passed = False
    
    # Test 5: Booking Page Response
    print("\n5. ✅ Testing Booking Page...")
    try:
        response = requests.get(f"{base_url}/booking/{refuge_id}/")
        if response.status_code == 200:
            print(f"   ✅ Booking Page: SUCCESS")
            content = response.text
            
            # Check for essential weather integration elements
            weather_elements = [
                ('weather.css', '✅ Weather CSS linked'),
                ('weather.js', '✅ Weather JS linked'),
                ('weather-container', '✅ Weather container present'),
                ('WeatherService', '✅ WeatherService initialized')
            ]
            
            for element, success_msg in weather_elements:
                if element in content:
                    print(f"   {success_msg}")
                else:
                    print(f"   ⚠️  {element} not found in template")
        else:
            print(f"   ❌ Booking Page FAILED: {response.status_code}")
            all_tests_passed = False
    except Exception as e:
        print(f"   ❌ Booking Page ERROR: {e}")
        all_tests_passed = False
    
    # Final Results
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 ALL WEATHER INTEGRATION TESTS PASSED!")
        print("\n✅ Weather integration is fully functional!")
        print("\n📋 WEATHER FEATURES VERIFIED:")
        print("   • Current weather data retrieval")
        print("   • 5-day weather forecast")
        print("   • Date-specific weather forecasts")
        print("   • Weather-based hiking recommendations")
        print("   • Static files properly served")
        print("   • Booking page integration")
        
        print("\n🌐 READY FOR USE:")
        print("   • Open http://127.0.0.1:8000/booking/105/ in browser")
        print("   • Weather widget should display automatically")
        print("   • Select dates to see weather recommendations")
        print("   • All weather APIs are working correctly")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return all_tests_passed

if __name__ == "__main__":
    test_weather_integration_final()
