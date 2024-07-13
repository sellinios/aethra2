import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.heat';

const MapComponent: React.FC = () => {
    const [temperatureData, setTemperatureData] = useState<any[]>([]);
    const [forecastHour, setForecastHour] = useState<number>(0);

    useEffect(() => {
        // Fetch weather data here
        const fetchData = async () => {
            try {
                const response = await fetch('/api/weather-data'); // Adjust the endpoint
                const data = await response.json();
                setTemperatureData(data);
            } catch (error) {
                console.error("Error fetching weather data:", error);
            }
        };

        fetchData();
    }, []);

    const HeatmapLayer = () => {
        const map = useMap();

        useEffect(() => {
            if (temperatureData.length) {
                const heatLayer = (L as any).heatLayer(
                    temperatureData.map((d: any) => [d.latitude, d.longitude, d.temperature - 273.15]), // Convert Kelvin to Celsius
                    { radius: 25 }
                ).addTo(map);

                return () => {
                    map.removeLayer(heatLayer);
                };
            }
        }, [temperatureData, map]);

        return null;
    };

    return (
        <div>
            <h1>Forecast Hour: {forecastHour}:00</h1>
            <MapContainer center={[38.638, 25.988]} zoom={7} style={{ height: '500px', width: '100%' }}>
                <TileLayer
                    url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
                />
                <HeatmapLayer />
            </MapContainer>
        </div>
    );
};

export default MapComponent;