// src/components/Weather/WeatherIcon.tsx
import React from 'react';
import {
  RseClearDay,
  RseClearNight,
  RseCloudy,
  RseFog,
  RseHail,
  RsePartlyCloudyDay,
  RsePartlyCloudyNight,
  RseRain,
  RseRainSnow,
  RseRainSnowShowersDay,
  RseRainSnowShowersNight,
  RseShowersDay,
  RseShowersNight,
  RseSleet,
  RseSnow,
  RseSnowShowersDay,
  RseSnowShowersNight,
  RseThunder,
  RseThunderRain,
  RseThunderShowersDay,
  RseThunderShowersNight,
  RseWind,
} from 'react-skycons-extended';

interface WeatherIconProps {
  state: string;
  width: number;
  height: number;
  color?: string;
  className?: string;
}

const WeatherIcon: React.FC<WeatherIconProps> = ({ state, width, height, color = 'black', className }) => {
  const getIconComponent = (state: string): React.FC<any> => {
    switch (state) {
      case 'sunny':
        return RseClearDay;
      case 'clear-night':
        return RseClearNight;
      case 'cloudy':
        return RseCloudy;
      case 'fog':
        return RseFog;
      case 'hail':
        return RseHail;
      case 'partlycloudy':
        return RsePartlyCloudyDay;
      case 'partlycloudy-night':
        return RsePartlyCloudyNight;
      case 'rain':
        return RseRain;
      case 'rainsnow':
        return RseRainSnow;
      case 'rainsnowshowersday':
        return RseRainSnowShowersDay;
      case 'rainsnowshowersnight':
        return RseRainSnowShowersNight;
      case 'showersday':
        return RseShowersDay;
      case 'showersnight':
        return RseShowersNight;
      case 'sleet':
        return RseSleet;
      case 'snow':
        return RseSnow;
      case 'snowshowersday':
        return RseSnowShowersDay;
      case 'snowshowersnight':
        return RseSnowShowersNight;
      case 'thunder':
        return RseThunder;
      case 'thunderrain':
        return RseThunderRain;
      case 'thundershowersday':
        return RseThunderShowersDay;
      case 'thundershowersnight':
        return RseThunderShowersNight;
      case 'wind':
        return RseWind;
      default:
        return RseCloudy;
    }
  };

  const IconComponent = getIconComponent(state);

  return (
    <div className={`weather-icon ${className}`}>
      <IconComponent
        color={color}
        width={width}
        height={height}
        autoplay={true}
      />
    </div>
  );
};

export default WeatherIcon;