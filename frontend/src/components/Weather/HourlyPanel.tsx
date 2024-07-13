import React from 'react';
import WeatherIcon from './WeatherIcon';
import './HourlyPanel.css';
import { Forecast } from '../../types';
import 'bootstrap/dist/css/bootstrap.min.css';
import { roundToNearestWhole, getWindDirection, getWeatherIconState, windSpeedToBeaufort, getPrecipitationType } from '../../utils/weatherUtils';

interface HourlyPanelProps {
  forecasts: Forecast[];
}

const HourlyPanel: React.FC<HourlyPanelProps> = ({ forecasts }) => {
  const currentDateTime = new Date();

  const filteredForecasts = forecasts.filter(forecast => {
    const forecastDateTime = new Date(`${forecast.date}T${String(forecast.hour).padStart(2, '0')}:00:00`);
    return forecastDateTime >= currentDateTime;
  });

  return (
    <div className="hourly-panel container">
      <div className="header">
        <div className="column">Hour</div>
        <div className="column">Temperature</div>
        <div className="column">Rain</div>
        <div className="column">Wind</div>
        <div className="column">Cloudiness</div>
      </div>
      {filteredForecasts.map((forecast) => {
        const roundedWindSpeed = Math.round(forecast.wind_speed || 0);
        const beaufortScale = windSpeedToBeaufort(roundedWindSpeed);
        const precipitationType = getPrecipitationType(
          forecast.forecast_data.precipitation_rate_level_0_surface,
          forecast.forecast_data.convective_precipitation_rate_level_0_surface
        );

        return (
          <div key={forecast.id} className="forecast-row">
            <div className="column">{String(forecast.hour).padStart(2, '0')}:00</div>
            <div className="column icon">
              <WeatherIcon
                state={getWeatherIconState(
                  forecast.state,
                  forecast.forecast_data.high_cloud_cover_level_0_highCloudLayer,
                  forecast.forecast_data.precipitation_rate_level_0_surface,
                  forecast.forecast_data.convective_precipitation_rate_level_0_surface ?? 0
                )}
                width={30}
                height={30}
              />
              {forecast.temperature_celsius !== null ? roundToNearestWhole(forecast.temperature_celsius) : 'N/A'} °C
            </div>
            <div className="column">{precipitationType}</div>
            <div className="column">
              {forecast.wind_speed !== null ? `${getWindDirection(forecast.wind_direction)} ${roundedWindSpeed} km/h (Beaufort: ${beaufortScale})` : 'N/A'}
            </div>
            <div className="column">
              {forecast.forecast_data.high_cloud_cover_level_0_highCloudLayer !== null ? `${roundToNearestWhole(forecast.forecast_data.high_cloud_cover_level_0_highCloudLayer)} %` : 'N/A'}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default HourlyPanel;