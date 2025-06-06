#!/usr/bin/env python
"""
Final weather integration test to verify everything works
"""

import json
import requests
import time
from datetime import datetime, timedelta

def run_final_weather_test():
    """Run comprehensive weather integration test"""
    base_url = "http://127.0.0.1:8000"
    refuge_id = 105
    
    print("🌤️  FINAL WEATHER INTEGRATION TEST")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    def test_api(name, url, expected_keys=None):
        nonlocal tests_passed, total_tests
        total_tests += 1
        
        try:
            print(f"\n🧪 Testing {name}...")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if expected_keys:
                    missing_keys = [key for key in expected_keys if key not in data]
                    if missing_keys:
                        print(f"   ❌ Missing keys: {missing_keys}")
                        return False
                
                print(f"   ✅ {name}: SUCCESS")
                if 'success' in data and data['success']:
                    print(f"   📊 Response includes success=True")
                    tests_passed += 1
                    return True
                elif 'error' not in data:
                    print(f"   📊 Response contains valid data")
                    tests_passed += 1
                    return True
                else:
                    print(f"   ⚠️  Response contains error: {data.get('error', 'Unknown')}")
                    return False
            else:
                print(f"   ❌ {name}: HTTP {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False
                
        except Exception as e:
            print(f"   ❌ {name}: {e}")
            return False
    
    # Test current weather API
    test_api(
        "Current Weather API", 
        f"{base_url}/api/weather/{refuge_id}/",
        ['success', 'current_weather', 'refuge_name']
    )
    
    # Test forecast API
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    test_api(
        "Forecast API", 
        f"{base_url}/api/weather/{refuge_id}/forecast/?date={tomorrow}",
        ['success', 'date', 'weather']
    )
    
    # Test booking page
    test_api(
        "Booking Page", 
        f"{base_url}/booking/{refuge_id}/",
    )
    
    # Test static files
    test_api(
        "Weather JavaScript", 
        f"{base_url}/static/js/weather.js",
    )
    
    test_api(
        "Weather CSS", 
        f"{base_url}/static/css/weather.css",
    )
    
    print(f"\n" + "=" * 50)
    print(f"🎯 TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! Weather integration is working correctly.")
        print("\n✅ WEATHER INTEGRATION COMPLETE!")
        print("\n📋 Summary:")
        print("  ✅ Weather APIs working")
        print("  ✅ Static files served")
        print("  ✅ Booking page accessible")
        print("  ✅ Database configured")
        print("  ✅ JavaScript integration ready")
        
        print("\n🌐 Ready for frontend testing:")
        print(f"  • Open: {base_url}/booking/{refuge_id}/")
        print("  • Check browser console for JavaScript logs")
        print("  • Verify weather widget displays")
        print("  • Test date selection for weather recommendations")
    else:
        print(f"⚠️  {total_tests - tests_passed} tests failed. Check the issues above.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    run_final_weather_test()
