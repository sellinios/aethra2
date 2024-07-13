// src/react-skycons-extended.d.ts
declare module 'react-skycons-extended' {
  import React from 'react';

  export type SkyconsType =
    | 'CLEAR_DAY'
    | 'CLEAR_NIGHT'
    | 'PARTLY_CLOUDY_DAY'
    | 'PARTLY_CLOUDY_NIGHT'
    | 'CLOUDY'
    | 'RAIN'
    | 'SLEET'
    | 'SNOW'
    | 'WIND'
    | 'FOG'
    | 'THUNDER'
    | 'THUNDER_RAIN'
    | 'THUNDER_SHOWERS_DAY'
    | 'THUNDER_SHOWERS_NIGHT'
    | 'RAIN_SNOW'
    | 'RAIN_SNOW_SHOWERS_DAY'
    | 'RAIN_SNOW_SHOWERS_NIGHT'
    | 'SHOWERS_DAY'
    | 'SHOWERS_NIGHT'
    | 'SNOW_SHOWERS_DAY'
    | 'SNOW_SHOWERS_NIGHT';

  export interface SkyconsProps {
    color?: string;
    type: SkyconsType;
    autoplay?: boolean;
    width?: number;
    height?: number;
    className?: string;
  }

  export const RseClearDay: React.FC<SkyconsProps>;
  export const RseClearNight: React.FC<SkyconsProps>;
  export const RseCloudy: React.FC<SkyconsProps>;
  export const RseFog: React.FC<SkyconsProps>;
  export const RseHail: React.FC<SkyconsProps>;
  export const RsePartlyCloudyDay: React.FC<SkyconsProps>;
  export const RsePartlyCloudyNight: React.FC<SkyconsProps>;
  export const RseRain: React.FC<SkyconsProps>;
  export const RseRainSnow: React.FC<SkyconsProps>;
  export const RseRainSnowShowersDay: React.FC<SkyconsProps>;
  export const RseRainSnowShowersNight: React.FC<SkyconsProps>;
  export const RseShowersDay: React.FC<SkyconsProps>;
  export const RseShowersNight: React.FC<SkyconsProps>;
  export const RseSleet: React.FC<SkyconsProps>;
  export const RseSnow: React.FC<SkyconsProps>;
  export const RseSnowShowersDay: React.FC<SkyconsProps>;
  export const RseSnowShowersNight: React.FC<SkyconsProps>;
  export const RseThunder: React.FC<SkyconsProps>;
  export const RseThunderRain: React.FC<SkyconsProps>;
  export const RseThunderShowersDay: React.FC<SkyconsProps>;
  export const RseThunderShowersNight: React.FC<SkyconsProps>;
  export const RseWind: React.FC<SkyconsProps>;
}