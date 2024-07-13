import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CookieConsent from 'react-cookie-consent';
import Footer from './components/Footer';
import UpperHeader from './components/UpperHeader';
import Header from './components/Header';
import WeatherPage from './pages/WeatherPage';
import HomePage from './pages/HomePage';
import Search from './components/Search';
import SearchResultsPage from './pages/SearchResultPage';
import Register from './components/Register';
import Login from './components/Login';
import AboutPage from './pages/AboutPage'; // Import AboutPage component
import ContactPage from './pages/ContactPage'; // Import ContactPage component
import GreekMunicipalities from './components/GreekMunicipalities';

const App: React.FC = () => {
    const [isConsentGiven, setIsConsentGiven] = useState(localStorage.getItem('cookieConsent') === 'true');

    const handleAccept = () => {
        localStorage.setItem('cookieConsent', 'true');
        setIsConsentGiven(true);
    };

    useEffect(() => {
        if (isConsentGiven) {
            // AdSense script is already in the HTML head, no need to add it here again.
        }
    }, [isConsentGiven]);

    return (
        <Router>
            <div>
                <UpperHeader />
                <Header />
                <Search />
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/about" element={<AboutPage />} />
                    <Route path="/contact" element={<ContactPage />} />
                    <Route path="/geography/greece/municipalities" element={<GreekMunicipalities />} />
                    <Route path="/weather/:continent/:country/:region/:subregion/:city" element={<WeatherPage />} />
                    <Route path="/search" element={<SearchResultsPage />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/login" element={<Login />} />
                </Routes>
                <Footer />
                <CookieConsent
                    location="bottom"
                    buttonText="I understand"
                    cookieName="myAwesomeCookieName2"
                    style={{ background: "#2B373B" }}
                    buttonStyle={{ color: "#4e503b", fontSize: "13px" }}
                    expires={150}
                    onAccept={handleAccept}
                >
                    This website uses cookies to enhance the user experience.
                </CookieConsent>
            </div>
        </Router>
    );
};

export default App;