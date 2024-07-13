import React, { useState } from 'react';
import WeatherIcon from './WeatherIcon';
import HourlyPanel from './HourlyPanel';
import { DailyForecast, Forecast } from '../../types';
import { FaExclamationTriangle, FaCheckCircle } from 'react-icons/fa';
import './HourlyPanel.css';
import './DailyPanel.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { roundToNearestWhole, getWindDirection, calculateTotalPrecipitation, getWeatherIconState, formatDate, windSpeedToBeaufort, getPrecipitationType } from '../../utils/weatherUtils';

interface DailyPanelProps {
  forecasts: DailyForecast[];
  country: string;
  showHeaders: boolean;
}

const DailyPanel: React.FC<DailyPanelProps> = ({ forecasts, country, showHeaders }) => {
  const [expandedDate, setExpandedDate] = useState<string | null>(null);
  const [showAll, setShowAll] = useState<boolean>(false);

  const toggleExpanded = (date: string) => {
    setExpandedDate(expandedDate === date ? null : date);
  };

  const toggleShowAll = () => {
    setShowAll(prevShowAll => !prevShowAll);
  };

  const getAlertMessage = (maxTemp: number, date: string) => {
    if (maxTemp > 40) {
      return (
        <div className="alert-zone alert-heatwave d-flex align-items-center justify-content-between w-100">
          <span className="d-flex align-items-center">
            <FaExclamationTriangle color="red" /> Heat Wave
          </span>
          <a href="#" onClick={() => toggleExpanded(date)} className="btn btn-primary btn-sm ml-3">
            Hourly
          </a>
        </div>
      );
    } else if (maxTemp > 35) {
      return (
        <div className="alert-zone alert-heat d-flex align-items-center justify-content-between w-100">
          <span className="d-flex align-items-center">
            <FaExclamationTriangle color="orange" /> Heat
          </span>
          <a href="#" onClick={() => toggleExpanded(date)} className="btn btn-primary btn-sm ml-3">
            Hourly
          </a>
        </div>
      );
    } else {
      return (
        <div className="alert-zone alert-no-alert d-flex align-items-center justify-content-between w-100">
          <span className="d-flex align-items-center">
            <FaCheckCircle color="green" /> No Alerts
          </span>
          <a href="#" onClick={() => toggleExpanded(date)} className="btn btn-primary btn-sm ml-3">
            Hourly
          </a>
        </div>
      );
    }
  };

  const currentDate = new Date();
  const startOfDay = new Date(currentDate.setHours(0, 0, 0, 0));
  const visibleForecasts = showAll ? forecasts : forecasts.slice(0, 7);
  const filteredForecasts = visibleForecasts.filter(({ date }) => new Date(date) >= startOfDay);

  const forecastComponents = filteredForecasts.map(({ date, generalText, maxTemp, minTemp, hourlyForecasts }) => {
    const totalPrecipitation = calculateTotalPrecipitation({ date, generalText, maxTemp, minTemp, hourlyForecasts });
    const generalIconState = getWeatherIconState(
      generalText,
      hourlyForecasts[0]?.forecast_data.high_cloud_cover_level_0_highCloudLayer || 0,
      hourlyForecasts[0]?.forecast_data.precipitation_rate_level_0_surface || 0,
      hourlyForecasts[0]?.forecast_data.convective_precipitation_rate_level_0_surface ?? 0
    );

    const alertMessage = getAlertMessage(maxTemp, date);

    const precipitationType = getPrecipitationType(
      hourlyForecasts[0]?.forecast_data.precipitation_rate_level_0_surface,
      hourlyForecasts[0]?.forecast_data.convective_precipitation_rate_level_0_surface
    );

    return (
      <div key={date} className="row mb-3 forecast-row">
        <div className="col-12">
          <div className="d-flex flex-wrap align-items-center forecast-details">
            <div className="col-md-2 col-sm-6 panel-date">{formatDate(date)}</div>
            <div className="col-md-1 col-sm-6 d-flex align-items-center justify-content-center">
              <WeatherIcon state={generalIconState} width={60} height={60} />
            </div>
            <div className="col-md-2 col-sm-6 temperature">
              <span className={maxTemp > 32 ? 'text-danger' : ''}>{roundToNearestWhole(maxTemp)}°C</span> / <span>{roundToNearestWhole(minTemp)}°C</span>
            </div>
            <div className="col-md-2 col-sm-6 wind-direction">
              {hourlyForecasts[0] && hourlyForecasts[0].wind_direction !== null && hourlyForecasts[0].wind_speed !== null && (
                <>
                  <span style={{ transform: `rotate(${hourlyForecasts[0].wind_direction}deg)` }}>↑</span>
                  {getWindDirection(hourlyForecasts[0].wind_direction)} {`${roundToNearestWhole(hourlyForecasts[0].wind_speed)} km/h (Beaufort: ${windSpeedToBeaufort(roundToNearestWhole(hourlyForecasts[0].wind_speed))})`}
                </>
              )}
            </div>
            <div className="col-md-2 col-sm-6 precipitation">
              Rain: {precipitationType}
            </div>
          </div>
          <div className="alert-line w-100 mt-2">{alertMessage}</div>
          {expandedDate === date && (
            <div className="expanded-section">
              <HourlyPanel forecasts={hourlyForecasts as Forecast[]} />
            </div>
          )}
          <hr />
        </div>
      </div>
    );
  });

  return (
    <div className="daily-panel container">
      {showHeaders && <h2 className="text-center my-4">Daily Weather Forecast for {country}</h2>}
      {forecastComponents}
      {forecasts.length > 7 && (
        <div className="text-center mt-3">
          <button className="btn btn-secondary" onClick={toggleShowAll}>
            {showAll ? 'Show Less' : 'Show More'}
          </button>
        </div>
      )}
    </div>
  );
};

export default DailyPanel;