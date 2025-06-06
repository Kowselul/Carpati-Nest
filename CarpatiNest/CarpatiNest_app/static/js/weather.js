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
            'Tornado': 'fas fa-tornado'
        };
        return iconMap[condition] || 'fas fa-cloud';
    }

    // Get weather recommendation based on weather data
    getWeatherRecommendation(weatherData) {
        const temp = weatherData.temperature;
        const condition = weatherData.description.toLowerCase();
        const windSpeed = weatherData.wind_speed || 0;
        const humidity = weatherData.humidity || 0;

        let recommendation = {
            rating: 'good',
            message: 'Perfect weather for hiking!',
            advice: []
        };

        // Temperature recommendations
        if (temp < -10) {
            recommendation.rating = 'poor';
            recommendation.message = 'Extremely cold conditions';
            recommendation.advice.push('Wear multiple layers and winter gear');
            recommendation.advice.push('Consider postponing outdoor activities');
        } else if (temp < 0) {
            recommendation.rating = 'fair';
            recommendation.message = 'Cold conditions - be prepared';
            recommendation.advice.push('Wear warm clothing and layers');
            recommendation.advice.push('Bring hot drinks and extra gear');
        } else if (temp > 30) {
            recommendation.rating = 'fair';
            recommendation.message = 'Hot conditions - stay hydrated';
            recommendation.advice.push('Bring plenty of water');
            recommendation.advice.push('Start early to avoid peak heat');
        }

        // Weather condition recommendations
        if (condition.includes('rain') || condition.includes('storm')) {
            recommendation.rating = 'poor';
            recommendation.message = 'Rainy conditions - not ideal for hiking';
            recommendation.advice.push('Bring waterproof gear');
            recommendation.advice.push('Check trail conditions before departing');
        } else if (condition.includes('snow')) {
            recommendation.rating = 'fair';
            recommendation.message = 'Snowy conditions - winter gear required';
            recommendation.advice.push('Bring winter hiking equipment');
            recommendation.advice.push('Check avalanche conditions');
        } else if (condition.includes('fog') || condition.includes('mist')) {
            recommendation.rating = 'fair';
            recommendation.message = 'Limited visibility - exercise caution';
            recommendation.advice.push('Bring navigation equipment');
            recommendation.advice.push('Stay on marked trails');
        }

        // Wind recommendations
        if (windSpeed > 15) {
            recommendation.rating = recommendation.rating === 'good' ? 'fair' : 'poor';
            recommendation.advice.push('Strong winds expected - secure all gear');
        }

        return recommendation;
    }

    // Fetch current weather for a refuge
    async fetchCurrentWeather(refugeId) {
        const cacheKey = `current_${refugeId}`;
        const cached = this.weatherCache.get(cacheKey);

        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/${refugeId}/`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            this.weatherCache.set(cacheKey, {
                data: data,
                timestamp: Date.now()
            });

            return data;
        } catch (error) {
            console.error('Error fetching current weather:', error);
            throw error;
        }
    }

    // Fetch weather forecast for a refuge
    async fetchWeatherForecast(refugeId, date = null) {
        const cacheKey = date ? `forecast_${refugeId}_${date}` : `forecast_${refugeId}`;
        const cached = this.weatherCache.get(cacheKey);

        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }

        try {
            let url = `${this.apiBaseUrl}/${refugeId}/forecast/`;
            if (date) {
                url += `?date=${date}`;
            }

            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            this.weatherCache.set(cacheKey, {
                data: data,
                timestamp: Date.now()
            });

            return data;
        } catch (error) {
            console.error('Error fetching weather forecast:', error);
            throw error;
        }
    }

    // Render current weather widget
    renderCurrentWeather(weatherData, containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container ${containerId} not found`);
            return;
        }

        const iconClass = this.getWeatherIcon(weatherData.description);
        const temperature = weatherData.temperature !== null ? `${weatherData.temperature}°C` : 'N/A';

        container.innerHTML = `
            <div class="weather-current">
                <div class="weather-icon">
                    <i class="${iconClass}"></i>
                </div>
                <div class="weather-info">
                    <div class="weather-temp">${temperature}</div>
                    <div class="weather-desc">${weatherData.description || 'N/A'}</div>
                    <div class="weather-location">${weatherData.location || 'Current Location'}</div>
                </div>
                <div class="weather-details">
                    <div class="weather-detail">
                        <i class="fas fa-wind"></i>
                        <span>${weatherData.wind_speed || 0} m/s</span>
                    </div>
                    <div class="weather-detail">
                        <i class="fas fa-tint"></i>
                        <span>${weatherData.humidity || 0}%</span>
                    </div>
                </div>
            </div>
        `;
    }

    // Render weather forecast
    renderWeatherForecast(forecastData, containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container ${containerId} not found`);
            return;
        }        if (!forecastData.forecast || !Array.isArray(forecastData.forecast)) {
            container.innerHTML = '<div class="forecast-error">No forecast data available</div>';
            return;
        }

        const forecastHTML = forecastData.forecast.map(forecast => {
            const iconClass = this.getWeatherIcon(forecast.description);
            const date = new Date(forecast.date).toLocaleDateString('en-US', {
                weekday: 'short',
                month: 'short',
                day: 'numeric'
            });            return `
                <div class="forecast-day">
                    <div class="forecast-date">${date}</div>
                    <div class="forecast-icon">
                        <i class="${iconClass}"></i>
                    </div>
                    <div class="forecast-temp">${forecast.min_temp}°/${forecast.max_temp}°C</div>
                    <div class="forecast-desc">${forecast.description}</div>
                </div>
            `;
        }).join('');

        container.innerHTML = `
            <div class="forecast-grid">
                ${forecastHTML}
            </div>
        `;
    }

    // Render weather recommendation for booking
    renderWeatherRecommendation(weatherData, containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container ${containerId} not found`);
            return;
        }

        const recommendation = this.getWeatherRecommendation(weatherData);
        const iconClass = this.getWeatherIcon(weatherData.description);
        const ratingClass = `rating-${recommendation.rating}`;

        const adviceHTML = recommendation.advice.length > 0
            ? `<div class="weather-advice">
                 <h5>Recommendations:</h5>
                 <ul>${recommendation.advice.map(advice => `<li>${advice}</li>`).join('')}</ul>
               </div>`
            : '';

        container.innerHTML = `
            <div class="weather-recommendation ${ratingClass}">
                <div class="recommendation-header">
                    <div class="weather-icon">
                        <i class="${iconClass}"></i>
                    </div>
                    <div class="weather-summary">
                        <div class="weather-temp">${weatherData.temperature}°C</div>
                        <div class="weather-desc">${weatherData.description}</div>
                        <div class="weather-rating ${ratingClass}">
                            <i class="fas fa-circle"></i>
                            <span>${recommendation.rating.toUpperCase()}</span>
                        </div>
                    </div>
                </div>
                <div class="recommendation-message">
                    <p>${recommendation.message}</p>
                </div>
                ${adviceHTML}
            </div>
        `;
    }

    // Initialize weather for booking page
    async initializeWeatherForBooking(refugeId) {
        try {
            // Hide loading and show content
            const loadingElement = document.getElementById('weather-loading');
            const weatherContainer = document.getElementById('weather-container');

            if (loadingElement) loadingElement.style.display = 'none';
            if (weatherContainer) weatherContainer.style.display = 'block';            // Fetch and render current weather
            const currentWeather = await this.fetchCurrentWeather(refugeId);
            this.renderCurrentWeather(currentWeather.current_weather, 'weather-container');

            // Fetch and render 5-day forecast
            const forecast = await this.fetchWeatherForecast(refugeId);
            this.renderWeatherForecast(forecast, 'forecast-container');

        } catch (error) {
            console.error('Error initializing weather:', error);

            // Show error message
            const weatherContainer = document.getElementById('weather-container');
            const loadingElement = document.getElementById('weather-loading');

            if (loadingElement) loadingElement.style.display = 'none';
            if (weatherContainer) {
                weatherContainer.style.display = 'block';
                weatherContainer.innerHTML = `
                    <div class="weather-error">
                        <i class="fas fa-exclamation-triangle"></i>
                        <p>Weather information temporarily unavailable</p>
                    </div>
                `;
            }
        }
    }

    // Update weather recommendation for selected date
    async updateWeatherForDate(refugeId, selectedDate) {
        try {
            const forecast = await this.fetchWeatherForecast(refugeId, selectedDate);
            if (forecast && forecast.forecasts && forecast.forecasts.length > 0) {
                this.renderWeatherRecommendation(forecast.forecasts[0], 'booking-weather-recommendation');
            }
        } catch (error) {
            console.error('Error updating weather for date:', error);
            const container = document.getElementById('booking-weather-recommendation');
            if (container) {
                container.innerHTML = `
                    <div class="weather-error">
                        <p>Unable to load weather forecast for selected date</p>
                    </div>
                `;
            }
        }
    }

    // Clear weather cache
    clearCache() {
        this.weatherCache.clear();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WeatherService;
}
