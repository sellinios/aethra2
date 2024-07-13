// src/utils/weatherUtils.ts
import { Forecast, DailyForecast, WeatherState } from '../types';

export const roundToNearestWhole = (num: number): number => {
  return Math.round(num);
};

export const getCardinalDirection = (angle: number | null): string => {
  if (angle === null) return 'N/A';
  const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
  const index = Math.floor((angle / 22.5) + 0.5) % 16;
  return directions[index];
};

export const calculateTotalPrecipitation = (daily: DailyForecast): number =>
  daily.hourlyForecasts.reduce((total: number, { forecast_data }) => total + (forecast_data.precipitation_rate_level_0_surface || 0), 0);

export const getWeatherIconState = (description: string, cloudCover: number | null, precipitation: number | null): WeatherState => {
  if (precipitation && precipitation > 0 || /rain|storm/.test(description.toLowerCase())) {
    return 'rainy';
  }
  if (/snow/.test(description.toLowerCase())) {
    return 'snowy';
  }
  if (/fog/.test(description.toLowerCase())) {
    return 'fog';
  }
  if (/hail/.test(description.toLowerCase())) {
    return 'hail';
  }
  if (/thunder/.test(description.toLowerCase())) {
    return 'lightning';
  }
  if (cloudCover !== null && cloudCover < 25) {
    return /night/.test(description.toLowerCase()) ? 'clear-night' : 'sunny';
  }
  if (cloudCover !== null && cloudCover < 50) {
    return 'partlycloudy';
  }
  return 'cloudy';
};

export const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  const options: Intl.DateTimeFormatOptions = { weekday: 'long', month: 'long', day: 'numeric' };
  return new Intl.DateTimeFormat('en-GB', options).format(date);
};

export const filterAndSortForecasts = (hourlyData: Forecast[]): Forecast[] => {
  const latestCycleMap: Record<string, Forecast> = {};

  hourlyData.forEach((forecast) => {
    const key = `${forecast.date}-${forecast.hour}`;
    if (!latestCycleMap[key] || new Date(forecast.timestamp) > new Date(latestCycleMap[key].timestamp)) {
      latestCycleMap[key] = forecast;
    }
  });

  const filteredData = Object.values(latestCycleMap);

  return filteredData.sort((a, b) => {
    if (a.date === b.date) {
      return a.hour - b.hour;
    }
    return new Date(a.date).getTime() - new Date(b.date).getTime();
  });
};

export const aggregateDailyData = (hourlyData: Forecast[]): DailyForecast[] => {
  const dailyDataMap: Record<string, DailyForecast> = {};

  hourlyData.forEach((data) => {
    const date = data.date;
    if (!dailyDataMap[date]) {
      dailyDataMap[date] = {
        date,
        generalText: 'General Text', // Replace this with actual generalText if available
        maxTemp: data.temperature_celsius,
        minTemp: data.temperature_celsius,
        hourlyForecasts: [],
      };
    }

    dailyDataMap[date].maxTemp = Math.max(dailyDataMap[date].maxTemp, data.temperature_celsius);
    dailyDataMap[date].minTemp = Math.min(dailyDataMap[date].minTemp, data.temperature_celsius);
    dailyDataMap[date].hourlyForecasts.push(data);
  });

  return Object.values(dailyDataMap);
};