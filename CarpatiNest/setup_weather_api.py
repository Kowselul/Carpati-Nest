#!/usr/bin/env python3
"""
Script pentru configurarea cheii API OpenWeatherMap
"""

import os
import webbrowser
from pathlib import Path

def setup_weather_api():
    """Ghid pas cu pas pentru configurarea API-ului meteo"""
    
    print("🌤️  CarpatiNest - Weather API Setup")
    print("="*50)
    print()
    
    # Verifică dacă există cheia API
    env_file = Path('.env')
    current_key = "demo-key-get-from-openweathermap"
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if 'WEATHER_API_KEY=' in content:
                for line in content.split('\n'):
                    if line.startswith('WEATHER_API_KEY='):
                        current_key = line.split('=', 1)[1]
                        break
    
    print(f"📋 Cheia API curentă: {current_key}")
    print()
    
    if current_key == "demo-key-get-from-openweathermap":
        print("⚠️  Folosești cheia demo. Pentru funcționalitate completă:")
        print()
        print("1. 🌐 Deschide site-ul OpenWeatherMap...")
        
        # Întreabă utilizatorul dacă vrea să deschidă site-ul
        open_site = input("   Deschid site-ul pentru tine? (y/n): ").lower().strip()
        
        if open_site in ['y', 'yes', 'da']:
            webbrowser.open('https://openweathermap.org/api')
            print("   ✅ Site-ul s-a deschis în browser")
        else:
            print("   🔗 Accesează manual: https://openweathermap.org/api")
        
        print()
        print("2. 📝 Pași pentru obținerea cheii API:")
        print("   a) Creează cont gratuit")
        print("   b) Mergi la 'My API Keys'")
        print("   c) Copiază 'Default' API key")
        print("   d) Cheia devine activă în ~10-15 minute")
        print()
        
        # Permite utilizatorului să introducă cheia
        new_key = input("3. 🔑 Introduci cheia API (sau Enter pentru mai târziu): ").strip()
        
        if new_key and new_key != current_key:
            update_env_file(new_key)
            print(f"   ✅ Cheia a fost salvată: {new_key[:10]}...")
            print("   ⏳ Așteaptă 10-15 minute pentru activare")
        else:
            print("   ℹ️  Poți actualiza cheia mai târziu în fișierul .env")
    else:
        print("✅ Cheia API este configurată!")
        
        # Testează cheia
        test_key = input("🧪 Testez cheia API? (y/n): ").lower().strip()
        if test_key in ['y', 'yes', 'da']:
            test_weather_api(current_key)
    
    print()
    print("📚 Pentru mai multe informații:")
    print("   - Citește WEATHER_INTEGRATION.md")
    print("   - Rulează: python test_weather_integration.py")
    print("   - Plan gratuit: 1000 requests/zi")
    print()

def update_env_file(new_api_key):
    """Actualizează cheia API în fișierul .env"""
    env_file = Path('.env')
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Înlocuiește cheia existentă
        lines = content.split('\n')
        updated = False
        
        for i, line in enumerate(lines):
            if line.startswith('WEATHER_API_KEY='):
                lines[i] = f'WEATHER_API_KEY={new_api_key}'
                updated = True
                break
        
        if not updated:
            lines.append(f'WEATHER_API_KEY={new_api_key}')
        
        with open(env_file, 'w') as f:
            f.write('\n'.join(lines))
    else:
        # Creează fișierul .env
        with open(env_file, 'w') as f:
            f.write(f'WEATHER_API_KEY={new_api_key}\n')

def test_weather_api(api_key):
    """Testează cheia API cu un request simplu"""
    try:
        import requests
        
        # Test coordonatele pentru Omu (Bucegi)
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': 45.4236,
            'lon': 25.4564,
            'appid': api_key,
            'units': 'metric',
            'lang': 'ro'
        }
        
        print("   ⏳ Testing API key...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            print(f"   ✅ API funcționează! Omu: {temp}°C, {desc}")
        elif response.status_code == 401:
            print("   ❌ Cheia API nu este validă sau nu este activă încă")
            print("   ⏳ Încearcă din nou în 10-15 minute")
        else:
            print(f"   ⚠️  Eroare API: {response.status_code}")
            
    except ImportError:
        print("   ⚠️  Modulul 'requests' nu este instalat")
        print("   💡 Rulează: pip install requests")
    except Exception as e:
        print(f"   ❌ Eroare la testare: {e}")

if __name__ == "__main__":
    setup_weather_api()
