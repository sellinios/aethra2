// src/components/Weather/CurrentPanel.tsx
import React from 'react';
import { Card } from 'react-bootstrap';
import { Forecast } from '../../types';
import './CurrentPanel.css';
import WeatherIcon from './WeatherIconC'; // Correct import
import { getWindDirection, getWeatherIconState, windSpeedToBeaufort, validateAndFormatCycleTime } from '../../utils/weatherUtils';

interface CurrentPanelProps {
  forecast: Forecast;
  nextForecasts: Forecast[];
}

const getColorForWeatherState = (state: string) => {
  switch (state) {
    case 'sunny':
      return 'yellow';
    case 'cloudy':
      return 'gray';
    case 'rainy':
      return 'blue';
    case 'snowy':
      return 'white';
    case 'fog':
      return 'lightgray';
    case 'lightning':
    case 'storm':
      return 'purple';
    case 'clear-night':
      return 'darkblue';
    case 'partlycloudy':
      return 'lightblue';
    case 'wind':
      return 'green';
    default:
      return 'black';
  }
};

const CurrentPanel: React.FC<CurrentPanelProps> = ({ forecast, nextForecasts }) => {
  console.log('Current forecast:', forecast);
  console.log('Next forecasts:', nextForecasts);

  const roundedWindSpeed = Math.round(forecast.wind_speed || 0);
  const beaufortScale = windSpeedToBeaufort(roundedWindSpeed);
  const validatedUtcCycleTime = validateAndFormatCycleTime(forecast.utc_cycle_time);

  const importedDate = new Date(forecast.imported_at);
  const modelCycleDate = `${importedDate.getUTCFullYear()}-${String(importedDate.getUTCMonth() + 1).padStart(2, '0')}-${String(importedDate.getUTCDate()).padStart(2, '0')} ${validatedUtcCycleTime}:00 UTC`;

  return (
    <Card className="mb-3 current-panel">
      <Card.Header className="current-panel-header">Current Weather</Card.Header>
      <Card.Body className="vertical-layout">
        {forecast.forecast_data ? (
          <>
            <WeatherIcon
              state={getWeatherIconState(
                forecast.state,
                forecast.forecast_data.high_cloud_cover_level_0_highCloudLayer,
                forecast.forecast_data.precipitation_rate_level_0_surface,
                forecast.forecast_data.convective_precipitation_rate_level_0_surface || 0
              )}
              width={100}
              height={100}
              color={getColorForWeatherState(forecast.state)} // Set color based on weather state
              className="weather-icon"
            />
            <Card.Title className="current-panel-title">{Math.round(forecast.temperature_celsius)}°C</Card.Title>
            <Card.Text>Wind: {roundedWindSpeed} km/h (Beaufort: {beaufortScale})</Card.Text>
            <Card.Text>Model Cycle: {modelCycleDate}</Card.Text>
          </>
        ) : (
          <Card.Text>Μη διαθέσιμο</Card.Text>
        )}
      </Card.Body>
      <Card.Body className="horizontal-layout">
        {nextForecasts.map((nextForecast) => {
          const nextRoundedWindSpeed = Math.round(nextForecast.wind_speed || 0);
          const nextBeaufortScale = windSpeedToBeaufort(nextRoundedWindSpeed);
          return (
            <div key={nextForecast.id} className="hourly-forecast">
              <div>{String(nextForecast.hour).padStart(2, '0')}:00</div>
              {nextForecast.forecast_data ? (
                <>
                  <WeatherIcon
                    state={getWeatherIconState(
                      nextForecast.state,
                      nextForecast.forecast_data.high_cloud_cover_level_0_highCloudLayer,
                      nextForecast.forecast_data.precipitation_rate_level_0_surface,
                      nextForecast.forecast_data.convective_precipitation_rate_level_0_surface || 0
                    )}
                    width={30}
                    height={30}
                    color={getColorForWeatherState(nextForecast.state)} // Set color based on weather state
                  />
                  <div>{Math.round(nextForecast.temperature_celsius)}°C</div>
                  <div>
                    {nextForecast.wind_speed ? (
                      <>
                        {`${getWindDirection(nextForecast.wind_direction)} ${nextRoundedWindSpeed} km/h (Beaufort: ${nextBeaufortScale})`}
                      </>
                    ) : (
                      'N/A'
                    )}
                  </div>
                </>
              ) : (
                <div>Μη διαθέσιμο</div>
              )}
            </div>
          );
        })}
      </Card.Body>
    </Card>
  );
};

export default CurrentPanel;