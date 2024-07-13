import { Forecast, DailyForecast, HourlyForecast, WeatherState } from '../types';

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
    dailyDataMap[date].hourlyForecasts.push(data as HourlyForecast); // Cast to HourlyForecast
  });

  return Object.values(dailyDataMap);
};

export const getVisibleDays = (width: number, dates: string[]) => {
  if (width >= 1200) {
    return dates.slice(0, 7); // Show 7 days on large screens
  } else if (width >= 992) {
    return dates.slice(0, 5); // Show 5 days on medium screens
  } else if (width >= 768) {
    return dates.slice(0, 3); // Show 3 days on small screens
  } else {
    return dates.slice(0, 2); // Show 2 days on extra small screens
  }
};

export const getWeatherIconState = (
  description: string | undefined,
  cloudCover: number | null,
  precipitation: number | null,
  convectivePrecipitation: number | null
): WeatherState => {
  if (convectivePrecipitation && convectivePrecipitation > 0) {
    return 'lightning';
  }
  if ((precipitation && precipitation > 0) || (description && /rain|storm/.test(description.toLowerCase()))) {
    return 'rainy';
  }
  if (description && /snow/.test(description.toLowerCase())) {
    return 'snowy';
  }
  if (description && /fog/.test(description.toLowerCase())) {
    return 'fog';
  }
  if (description && /hail/.test(description.toLowerCase())) {
    return 'hail';
  }
  if (description && /thunder/.test(description.toLowerCase())) {
    return 'lightning';
  }
  if (cloudCover !== null && cloudCover < 25) {
    return description && /night/.test(description.toLowerCase()) ? 'clear-night' : 'sunny';
  }
  if (cloudCover !== null && cloudCover < 50) {
    return 'partlycloudy';
  }
  return 'cloudy';
};

export const getWindDirection = (angle: number | null): string => {
  if (angle === null) return 'N/A';
  const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
  const index = Math.floor((angle / 22.5) + 0.5) % 16;
  return directions[index];
};

export const calculateTotalPrecipitation = (daily: DailyForecast): number =>
  daily.hourlyForecasts.reduce((total: number, { forecast_data }) => total + (forecast_data.precipitation_rate_level_0_surface || 0), 0);

export const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  const options: Intl.DateTimeFormatOptions = { weekday: 'long', month: 'long', day: 'numeric' };
  return new Intl.DateTimeFormat('en-GB', options).format(date);
};

export const roundToNearestWhole = (num: number): number => {
  return Math.round(num);
};

export const windSpeedToBeaufort = (speed: number) => {
  if (speed < 1) return 0;
  else if (speed <= 5) return 1;
  else if (speed <= 11) return 2;
  else if (speed <= 19) return 3;
  else if (speed <= 28) return 4;
  else if (speed <= 38) return 5;
  else if (speed <= 49) return 6;
  else if (speed <= 61) return 7;
  else if (speed <= 74) return 8;
  else if (speed <= 88) return 9;
  else if (speed <= 102) return 10;
  else if (speed <= 117) return 11;
  else return 12;
};

export const validateAndFormatCycleTime = (utcCycleTime: string): string => {
  const validCycleTimes = ['00', '06', '12', '18'];
  return validCycleTimes.includes(utcCycleTime) ? utcCycleTime : '00';
};

export const getPrecipitationType = (
  precipitation: number | null | undefined,
  convectivePrecipitation: number | null | undefined
): string => {
  const roundedPrecipitation = precipitation !== null && precipitation !== undefined
    ? roundToNearestWhole(precipitation)
    : convectivePrecipitation !== null && convectivePrecipitation !== undefined
    ? roundToNearestWhole(convectivePrecipitation)
    : 'N/A';

  const isTrace = roundedPrecipitation === 0 && ((precipitation ?? 0) > 0 || (convectivePrecipitation ?? 0) > 0);

  if (isTrace) {
    if ((precipitation ?? 0) > 0) {
      return 'Trace (Precipitation)';
    }
    return 'Trace (Convective)';
  }

  return `${roundedPrecipitation} mm/h`;
};