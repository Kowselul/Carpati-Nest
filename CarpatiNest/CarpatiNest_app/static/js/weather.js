// Weather Service JavaScript
class WeatherService {
    constructor() {
        this.apiBaseUrl = '/api/weather';
        this.weatherCache = new Map();
        this.cacheTimeout = 10 * 60 * 1000; // 10 minutes
    }

    // Get weather icons based on weather condition
    getWeatherIcon(condition, isDay = true) {
        const iconMap = {
            'Clear': isDay ? 'fas fa-sun' : 'fas fa-moon',
            'Clouds': 'fas fa-cloud',
            'Rain': 'fas fa-cloud-rain',
            'Drizzle': 'fas fa-cloud-drizzle',
            'Thunderstorm': 'fas fa-bolt',
            'Snow': 'fas fa-snowflake',
            'Mist': 'fas fa-smog',
            'Smoke': 'fas fa-smog',
            'Haze': 'fas fa-smog',
            'Dust': 'fas fa-smog',
            'Fog': 'fas fa-smog',
            'Sand': 'fas fa-smog',
            'Ash': 'fas fa-smog',
            'Squall': 'fas fa-wind',
            'Tornado': 'fas fa-wind'
        };
        return iconMap[condition] || 'fas fa-cloud';
    }

    // Get hiking recommendation icon and color
    getHikingRecommendationStyle(recommendation) {
        const styles = {
            'Excelent pentru drumeții': { icon: 'fas fa-hiking', class: 'good' },
            'Bun pentru drumeții': { icon: 'fas fa-hiking', class: 'good' },
            'Acceptabil pentru drumeții': { icon: 'fas fa-exclamation-triangle', class: 'fair' },
            'Nu este recomandat': { icon: 'fas fa-times-circle', class: 'poor' },
            'Periculos': { icon: 'fas fa-exclamation-triangle', class: 'poor' }
        };
        return styles[recommendation] || { icon: 'fas fa-question-circle', class: 'fair' };
    }

    // Cache management
    getCachedWeather(refugeId) {
        const cached = this.weatherCache.get(refugeId);
        if (cached && (Date.now() - cached.timestamp) < this.cacheTimeout) {
            return cached.data;
        }
        return null;
    }

    setCachedWeather(refugeId, data) {
        this.weatherCache.set(refugeId, {
            data: data,
            timestamp: Date.now()
        });
    }

    // Fetch weather data for refuge
    async fetchWeatherData(refugeId) {
        // Check cache first
        const cached = this.getCachedWeather(refugeId);
        if (cached) {
            return cached;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/${refugeId}/`);
            const data = await response.json();
            
            if (data.success) {
                this.setCachedWeather(refugeId, data);
                return data;
            } else {
                throw new Error(data.error || 'Eroare la obținerea datelor meteo');
            }
        } catch (error) {
            console.error('Weather fetch error:', error);
            throw error;
        }
    }

    // Fetch weather forecast for specific date
    async fetchWeatherForDate(refugeId, date) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/${refugeId}/forecast/?date=${date}`);
            const data = await response.json();
            
            if (data.success) {
                return data;
            } else {
                throw new Error(data.error || 'Eroare la obținerea prognozei meteo');
            }
        } catch (error) {
            console.error('Weather forecast fetch error:', error);
            throw error;
        }
    }

    // Render weather widget
    renderWeatherWidget(container, weatherData) {
        const current = weatherData.current_weather;
        const recommendation = weatherData.hiking_recommendation;
        const alerts = weatherData.alerts;

        const iconClass = this.getWeatherIcon(current.weather[0].main);
        const recStyle = this.getHikingRecommendationStyle(recommendation.recommendation);

        const alertsHtml = alerts && alerts.length > 0 ? 
            `<div class="weather-alerts show">
                <div class="alert-title">
                    <i class="fas fa-exclamation-triangle"></i>
                    Alertă meteo
                </div>
                <div class="alert-description">
                    ${alerts.map(alert => alert.description).join(', ')}
                </div>
            </div>` : '';

        const html = `
            <div class="weather-widget weather-fade-in">
                <div class="weather-header">
                    <h3 class="weather-title">
                        <i class="fas fa-cloud-sun"></i>
                        Vremea curentă
                    </h3>
                </div>
                
                <div class="weather-current">
                    <div class="weather-icon ${iconClass.replace('fas fa-', '')}">
                        <i class="${iconClass}"></i>
                    </div>
                    
                    <div class="weather-main">
                        <div class="weather-temp">${Math.round(current.main.temp)}°C</div>
                        <div class="weather-description">${current.weather[0].description}</div>
                        <div class="weather-feels-like">Se simte ca ${Math.round(current.main.feels_like)}°C</div>
                    </div>
                </div>
                
                <div class="weather-details">
                    <div class="weather-detail">
                        <div class="weather-detail-label">Umiditate</div>
                        <div class="weather-detail-value">${current.main.humidity}%</div>
                    </div>
                    <div class="weather-detail">
                        <div class="weather-detail-label">Vânt</div>
                        <div class="weather-detail-value">${Math.round(current.wind.speed * 3.6)} km/h</div>
                    </div>
                    <div class="weather-detail">
                        <div class="weather-detail-label">Presiune</div>
                        <div class="weather-detail-value">${current.main.pressure} hPa</div>
                    </div>
                    <div class="weather-detail">
                        <div class="weather-detail-label">Vizibilitate</div>
                        <div class="weather-detail-value">${current.visibility ? (current.visibility / 1000).toFixed(1) : 'N/A'} km</div>
                    </div>
                </div>
                
                <div class="hiking-recommendation">
                    <div class="hiking-status ${recStyle.class}">
                        <i class="${recStyle.icon}"></i>
                        ${recommendation.recommendation}
                    </div>
                    <div class="hiking-details">
                        ${recommendation.details}
                    </div>
                </div>
                
                ${alertsHtml}
            </div>
        `;

        container.innerHTML = html;
    }

    // Render forecast widget
    renderForecastWidget(container, forecastData) {
        const forecast = forecastData.forecast;
        
        if (!forecast || !forecast.daily) {
            container.innerHTML = '<div class="weather-error">Nu sunt disponibile date de prognoză</div>';
            return;
        }

        const forecastDays = forecast.daily.slice(0, 5); // Show 5 days
        
        const forecastHtml = forecastDays.map(day => {
            const date = new Date(day.dt * 1000);
            const dayName = date.toLocaleDateString('ro-RO', { weekday: 'short', day: 'numeric', month: 'short' });
            const iconClass = this.getWeatherIcon(day.weather[0].main);
            
            return `
                <div class="forecast-day">
                    <div class="forecast-date">${dayName}</div>
                    <div class="forecast-icon">
                        <i class="${iconClass}"></i>
                    </div>
                    <div class="forecast-temps">
                        <span class="forecast-high">${Math.round(day.temp.max)}°</span>
                        <span class="forecast-low">${Math.round(day.temp.min)}°</span>
                    </div>
                    <div class="forecast-desc">${day.weather[0].description}</div>
                </div>
            `;
        }).join('');

        const html = `
            <div class="weather-forecast weather-fade-in">
                <h3 class="forecast-title">
                    <i class="fas fa-calendar-week"></i>
                    Prognoza pe 5 zile
                </h3>
                <div class="forecast-grid">
                    ${forecastHtml}
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    // Show loading state
    showWeatherLoading(container) {
        container.innerHTML = `
            <div class="weather-loading">
                <div class="weather-spinner"></div>
                <span>Se încarcă datele meteo...</span>
            </div>
        `;
    }

    // Show error state
    showWeatherError(container, error) {
        container.innerHTML = `
            <div class="weather-error">
                <i class="fas fa-exclamation-circle"></i>
                <span>Eroare la încărcarea datelor meteo: ${error}</span>
            </div>
        `;
    }

    // Show unavailable state
    showWeatherUnavailable(container) {
        container.innerHTML = `
            <div class="weather-unavailable">
                <i class="fas fa-cloud-slash"></i>
                <p>Datele meteo nu sunt disponibile pentru acest refugiu</p>
                <small>Coordonatele GPS nu sunt configurate</small>
            </div>
        `;
    }

    // Initialize weather for booking page
    async initializeWeatherForBooking(refugeId) {
        const weatherContainer = document.getElementById('weather-container');
        const forecastContainer = document.getElementById('forecast-container');
        
        if (!weatherContainer) {
            console.warn('Weather container not found');
            return;
        }

        try {
            this.showWeatherLoading(weatherContainer);
            
            const weatherData = await this.fetchWeatherData(refugeId);
            
            if (weatherData.has_coordinates) {
                this.renderWeatherWidget(weatherContainer, weatherData);
                
                if (forecastContainer) {
                    this.renderForecastWidget(forecastContainer, weatherData);
                }
                
                // Update booking recommendation based on weather
                this.updateBookingRecommendation(weatherData);
            } else {
                this.showWeatherUnavailable(weatherContainer);
            }
            
        } catch (error) {
            this.showWeatherError(weatherContainer, error.message);
        }
    }

    // Update booking recommendation based on weather
    updateBookingRecommendation(weatherData) {
        const bookingWeatherSection = document.querySelector('.booking-weather-section');
        
        if (!bookingWeatherSection) return;

        const recommendation = weatherData.hiking_recommendation;
        const recStyle = this.getHikingRecommendationStyle(recommendation.recommendation);
        
        let alertClass = '';
        if (recStyle.class === 'poor') {
            alertClass = 'danger';
        } else if (recStyle.class === 'fair') {
            alertClass = 'warning';
        }

        const html = `
            <div class="weather-booking-header">
                <i class="${recStyle.icon}"></i>
                <h4>Recomandare pentru drumeții</h4>
            </div>
            <div class="weather-booking-recommendation ${alertClass}">
                <strong>${recommendation.recommendation}</strong>
                <p>${recommendation.details}</p>
            </div>
        `;

        bookingWeatherSection.innerHTML = html;
    }

    // Check weather for selected date
    async checkWeatherForDate(refugeId, selectedDate) {
        try {
            const weatherData = await this.fetchWeatherForDate(refugeId, selectedDate);
            
            if (weatherData.success) {
                this.updateDateWeatherInfo(weatherData);
            }
        } catch (error) {
            console.error('Error checking weather for date:', error);
        }
    }

    // Update weather info for selected date
    updateDateWeatherInfo(weatherData) {
        const dateWeatherInfo = document.getElementById('date-weather-info');
        
        if (!dateWeatherInfo) return;

        const weather = weatherData.weather;
        const iconClass = this.getWeatherIcon(weather.weather[0].main);
        
        const suitabilityClass = weatherData.hiking_suitable ? 'good' : 'poor';
        const suitabilityIcon = weatherData.hiking_suitable ? 'fas fa-check-circle' : 'fas fa-exclamation-triangle';
        
        const html = `
            <div class="date-weather-info weather-fade-in">
                <div class="date-weather-summary">
                    <i class="${iconClass}"></i>
                    <span>${Math.round(weather.temp.day)}°C - ${weather.weather[0].description}</span>
                </div>
                <div class="date-hiking-status ${suitabilityClass}">
                    <i class="${suitabilityIcon}"></i>
                    <span>${weatherData.hiking_suitable ? 'Potrivit pentru drumeții' : 'Nu este recomandat'}</span>
                </div>
            </div>
        `;

        dateWeatherInfo.innerHTML = html;
    }
}

// Initialize weather service when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.weatherService = new WeatherService();
    
    // Initialize weather for booking page if refuge ID is available
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        const refugeId = bookingForm.getAttribute('data-refuge-id');
        if (refugeId) {
            window.weatherService.initializeWeatherForBooking(refugeId);
        }
    }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WeatherService;
}
