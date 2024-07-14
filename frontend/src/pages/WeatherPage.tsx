// src/pages/WeatherPage.tsx

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';
import { isAxiosError, getAxiosErrorMessage } from '../utils/axios.Error';
import DailyPanel from '../components/Weather/DailyPanel';
import CurrentPanel from '../components/Weather/CurrentPanel';
import { Container, Alert, Spinner } from 'react-bootstrap';
import './WeatherPage.css';
import '../components/Weather/HourlyPanel.css';
import '../components/Weather/DailyPanel.css';
import { Forecast, DailyForecast } from '../types';
import { filterAndSortForecasts, aggregateDailyData } from '../utils/weatherUtils';

interface RouteParams extends Record<string, string | undefined> {
  continent: string;
  country: string;
  region: string;
  subregion: string;
  city: string;
}

const capitalizeFirstLetter = (string: string) => {
  return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
};

const WeatherPage: React.FC = () => {
  const { continent, country, region, subregion, city } = useParams<RouteParams>();
  const [hourlyWeatherData, setHourlyWeatherData] = useState<Forecast[]>([]);
  const [dailyWeatherData, setDailyWeatherData] = useState<DailyForecast[]>([]);
  const [currentWeatherData, setCurrentWeatherData] = useState<Forecast | null>(null);
  const [nextWeatherData, setNextWeatherData] = useState<Forecast[]>([]); // Add state for next forecasts
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchWeatherData = async () => {
      setLoading(true);
      try {
        const response = await axiosInstance.get(`/en/weather/${continent}/${country}/${region}/${subregion}/${city}/`);
        const hourlyData: Forecast[] = response.data.forecasts;
        const currentDate = new Date();

        const filteredData = filterAndSortForecasts(hourlyData).filter(forecast => {
          const forecastDateTime = new Date(`${forecast.date}T${String(forecast.hour).padStart(2, '0')}:00:00`);
          return forecastDateTime >= currentDate || forecast.date > currentDate.toISOString().split('T')[0];
        });

        const aggregatedData = aggregateDailyData(filteredData);
        setHourlyWeatherData(filteredData);
        setDailyWeatherData(aggregatedData);
        setCurrentWeatherData(filteredData[0]);
        setNextWeatherData(filteredData.slice(1, 4)); // Set the next few hours of forecasts
        setError(null);
      } catch (err: unknown) {
        console.error('Error fetching weather data:', err);
        if (isAxiosError(err)) {
          setError(getAxiosErrorMessage(err));
        } else {
          setError('Unknown error');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchWeatherData();
  }, [continent, country, region, subregion, city]);

  return (
    <Container>
      <h1 className="text-center my-4">Weather for {capitalizeFirstLetter(city || '')}</h1>
      {loading && (
        <div className="text-center">
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
          </Spinner>
        </div>
      )}
      {error && <Alert variant="danger">{error}</Alert>}
      {currentWeatherData && <CurrentPanel forecast={currentWeatherData} nextForecasts={nextWeatherData} />}
      {dailyWeatherData.length > 0 && <DailyPanel forecasts={dailyWeatherData} country={city || 'Unknown'} showHeaders={false} />}
    </Container>
  );
};

export default WeatherPage;

export {};