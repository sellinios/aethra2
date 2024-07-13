// src/types.ts

export type WeatherState =
  | 'sunny'
  | 'clear-night'
  | 'partlycloudy'
  | 'cloudy'
  | 'fog'
  | 'hail'
  | 'rainy'
  | 'snowy'
  | 'snowy-rainy'
  | 'pouring'
  | 'lightning'
  | 'lightning-rainy'
  | 'windy'
  | 'windy-variant';

export interface ForecastData {
  precipitation_rate_level_0_surface: number;
  low_cloud_cover_level_0_lowCloudLayer: number;
  temperature_level_2_heightAboveGround: number;
  high_cloud_cover_level_0_highCloudLayer: number;
  medium_cloud_cover_level_0_middleCloudLayer: number;
  u_component_of_wind_level_10_heightAboveGround: number | null;
  v_component_of_wind_level_10_heightAboveGround: number | null;
  total_precipitation_level_0_surface?: number;
  convective_precipitation_level_0_surface?: number;
  convective_precipitation_rate_level_0_surface?: number; // Corrected typo
  maximum_temperature_level_2_heightAboveGround?: number;
  minimum_temperature_level_2_heightAboveGround?: number;
  convective_available_potential_energy_level_0_surface?: number;
}

export interface Forecast {
  id: number;
  latitude: number;
  longitude: number;
  temperature_celsius: number;
  wind_speed: number | null;
  wind_direction: number | null;
  forecast_data: ForecastData;
  date: string;
  hour: number;
  timestamp: string;
  utc_cycle_time: string;
  imported_at: string;
  state: WeatherState;
}

export interface HourlyForecast {
  date: string;
  hour: number;
  temperature_celsius: number;
  wind_speed: number | null;
  wind_direction: number | null;
  forecast_data: ForecastData;
}
export interface DailyForecast {
  date: string;
  maxTemp: number;
  minTemp: number;
  generalText: string;
  high_cloud_cover_level_0_highCloudLayer?: number;
  precipitation_rate_level_0_surface?: number;
  convective_precipitation_rate_level_0_surface?: number;
  hourlyForecasts: HourlyForecast[];
}

export interface CityWeather {
  city: string;
  forecasts: DailyForecast[];
}