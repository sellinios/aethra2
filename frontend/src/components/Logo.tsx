// src/components/Logo.tsx
import React from 'react';
import WeatherIcon from './Weather/WeatherIcon'; // Ensure this is the correct import

const Logo: React.FC = () => {
    const logoStyle: React.CSSProperties = {
        display: 'flex',
        alignItems: 'center',
        padding: '10px',
        borderRadius: '5px',
    };

    const textContainerStyle: React.CSSProperties = {
        display: 'flex',
        flexDirection: 'column',
        marginRight: '10px',
    };

    const mainTextStyle: React.CSSProperties = {
        fontSize: '40px',
        color: 'lightskyblue',
        margin: 0,
    };

    const subTextStyle: React.CSSProperties = {
        fontSize: '15px',
        color: 'white',
        marginTop: '-5px',
    };

    return (
        <div style={logoStyle}>
            <div style={textContainerStyle}>
                <div style={mainTextStyle}>Kairos</div>
                <div style={subTextStyle}>www.kairos.gr</div>
            </div>
            <WeatherIcon state="wind" width={60} height={60} color="orange" />
        </div>
    );
};

export default Logo;