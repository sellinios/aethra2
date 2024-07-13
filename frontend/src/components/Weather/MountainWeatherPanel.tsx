import React from 'react';
import { Card } from 'react-bootstrap';
import { Forecast } from '../../types';
import WeatherIcon from './WeatherIcon';
import { getWindDirection, getWeatherIconState, windSpeedToBeaufort, validateAndFormatCycleTime } from '../../utils/weatherUtils';

interface MountainWeatherPanelProps {
  forecast: Forecast;
  nextForecasts: Forecast[];
}

const MountainWeatherPanel: React.FC<MountainWeatherPanelProps> = ({ forecast, nextForecasts }) => {
  const roundedWindSpeed = Math.round(forecast.wind_speed || 0);
  const beaufortScale = windSpeedToBeaufort(roundedWindSpeed);
  const validatedUtcCycleTime = validateAndFormatCycleTime(forecast.utc_cycle_time);

  const importedDate = new Date(forecast.imported_at);
  const modelCycleDate = `${importedDate.getUTCFullYear()}-${String(importedDate.getUTCMonth() + 1).padStart(2, '0')}-${String(importedDate.getUTCDate()).padStart(2, '0')} ${validatedUtcCycleTime}:00 UTC`;

  return (
    <Card className="mb-3 mountain-weather-panel">
      <Card.Header className="mountain-weather-panel-header">Mountain Weather</Card.Header>
      <Card.Body className="vertical-layout">
        <WeatherIcon
          state={getWeatherIconState(
            forecast.state,
            forecast.forecast_data.high_cloud_cover_level_0_highCloudLayer,
            forecast.forecast_data.precipitation_rate_level_0_surface,
            forecast.forecast_data.convective_precipitation_rate_level_0_surface || 0
          )}
          width={100}
          height={100}
          className="weather-icon"
        />
        <Card.Title className="mountain-weather-panel-title">{Math.round(forecast.temperature_celsius)}°C</Card.Title>
        <Card.Text>Wind: {roundedWindSpeed} km/h (Beaufort: {beaufortScale})</Card.Text>
        <Card.Text>Model Cycle: {modelCycleDate}</Card.Text>
      </Card.Body>
      <Card.Body className="horizontal-layout">
        {nextForecasts.map((nextForecast) => {
          const nextRoundedWindSpeed = Math.round(nextForecast.wind_speed || 0);
          const nextBeaufortScale = windSpeedToBeaufort(nextRoundedWindSpeed);
          return (
            <div key={nextForecast.id} className="hourly-forecast">
              <div>{String(nextForecast.hour).padStart(2, '0')}:00</div>
              <WeatherIcon
                state={getWeatherIconState(
                  nextForecast.state,
                  nextForecast.forecast_data.high_cloud_cover_level_0_highCloudLayer,
                  nextForecast.forecast_data.precipitation_rate_level_0_surface,
                  nextForecast.forecast_data.convective_precipitation_rate_level_0_surface || 0
                )}
                width={30}
                height={30}
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
            </div>
          );
        })}
      </Card.Body>
    </Card>
  );
};

export default MountainWeatherPanel;