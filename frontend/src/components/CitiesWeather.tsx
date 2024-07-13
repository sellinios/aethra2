import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table, Spinner, Alert } from 'react-bootstrap';
import WeatherIcon from './Weather/WeatherIcon';
import { DailyForecast, CityWeather } from '../types';
import './CitiesWeather.css';
import { filterAndSortForecasts, aggregateDailyData, getVisibleDays, getWeatherIconState } from '../utils/weatherUtils';
import { useTranslation } from 'react-i18next';

const CitiesWeather: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [weatherData, setWeatherData] = useState<CityWeather[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [visibleDays, setVisibleDays] = useState<string[]>([]);

  useEffect(() => {
    const handleResize = () => {
      const sortedDates = Array.from(new Set(weatherData.flatMap(cityWeather => cityWeather.forecasts.map(forecast => forecast.date))))
        .sort((a, b) => new Date(a).getTime() - new Date(b).getTime())
        .filter(date => date >= currentDate);
      setVisibleDays(getVisibleDays(window.innerWidth, sortedDates));
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Set initial state

    return () => window.removeEventListener('resize', handleResize);
  }, [weatherData]);

  useEffect(() => {
    const langCode = i18n.language; // Get the current language
    const cities = ['athens', 'thessaloniki', 'patra']; // Update city slugs here
    const fetchWeatherData = async () => {
      try {
        const cityWeatherPromises = cities.map(async (city) => {
          const response = await axios.get(`/api/${langCode}/weather/cities/?cities=${city}`);
          const hourlyData = response.data[0]?.forecasts || [];

          // Filter and sort the forecasts
          const filteredData = filterAndSortForecasts(hourlyData);
          const aggregatedData = aggregateDailyData(filteredData);

          return { city: response.data[0]?.city || city, forecasts: aggregatedData };
        });

        const cityWeatherData = await Promise.all(cityWeatherPromises);
        setWeatherData(cityWeatherData);
        setError(null);
      } catch (err) {
        setError(t('error_fetching_weather_data'));
      } finally {
        setLoading(false);
      }
    };

    fetchWeatherData();
  }, [i18n.language]);

  const currentDate = new Date().toISOString().split('T')[0];
  const sortedDates = Array.from(new Set(weatherData.flatMap(cityWeather => cityWeather.forecasts.map(forecast => forecast.date))))
    .sort((a, b) => new Date(a).getTime() - new Date(b).getTime())
    .filter(date => date >= currentDate);

  const cityLinks: { [key: string]: string } = {
    athens: 'http://kairos.gr/weather/europe/greece/attica/municipality-of-athens/athens/',
    patra: 'http://kairos.gr/weather/europe/greece/peloponnese/municipality-of-patras/patra/',
    thessaloniki: 'http://kairos.gr/weather/europe/greece/central-macedonia/municipality-of-thessaloniki/thessaloniki/'
  };

  return (
    <div className="container">
      {loading && <Spinner animation="border" />}
      {error && <Alert variant="danger">{error}</Alert>}
      {!loading && !error && (
        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>{t('city')}</th>
              {visibleDays.map((date, index) => (
                <th key={index}>{new Date(date).toLocaleDateString(i18n.language, { weekday: 'long', day: 'numeric', month: 'long' })}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {weatherData.map((cityWeather, index) => (
              <tr key={index}>
                <td>
                  <a href={cityLinks[cityWeather.city.toLowerCase()]} target="_blank" rel="noopener noreferrer">
                    {t(cityWeather.city.toLowerCase())}
                  </a>
                </td>
                {visibleDays.map((date, index) => {
                  const forecast = cityWeather.forecasts.find(forecast => forecast.date === date);

                  if (!forecast) {
                    return <td key={index} className="text-center">{t('na')}</td>;
                  }

                  const weatherIconState = getWeatherIconState(
                    forecast.generalText,
                    forecast.hourlyForecasts[0]?.forecast_data.high_cloud_cover_level_0_highCloudLayer || 0,
                    forecast.hourlyForecasts[0]?.forecast_data.precipitation_rate_level_0_surface || 0,
                    forecast.hourlyForecasts[0]?.forecast_data.convective_precipitation_rate_level_0_surface || 0
                  );

                  return (
                    <td key={index} className="text-center">
                      {`${Math.round(forecast.maxTemp)}°C / ${Math.round(forecast.minTemp)}°C`}
                      <br />
                      <WeatherIcon state={weatherIconState} width={24} height={24} />
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </div>
  );
};

export default CitiesWeather;