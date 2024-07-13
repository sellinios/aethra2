// src/components/LanguageSwitcher.tsx
import React from 'react';
import { useTranslation } from 'react-i18next';
import { Dropdown } from 'react-bootstrap';
import { FaCog } from 'react-icons/fa';

const LanguageSwitcher: React.FC = () => {
    const { i18n } = useTranslation();

    const changeLanguage = (lng: string) => {
        i18n.changeLanguage(lng);
    };

    return (
        <Dropdown>
            <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                <FaCog />
            </Dropdown.Toggle>

            <Dropdown.Menu>
                <Dropdown.Item onClick={() => changeLanguage('en')}>English</Dropdown.Item>
                <Dropdown.Item onClick={() => changeLanguage('fr')}>Français</Dropdown.Item>
                <Dropdown.Item onClick={() => changeLanguage('el')}>Ελληνικά</Dropdown.Item>
                <Dropdown.Item onClick={() => changeLanguage('es')}>Español</Dropdown.Item>
                <Dropdown.Item onClick={() => changeLanguage('de')}>Deutsch</Dropdown.Item>
                <Dropdown.Item onClick={() => changeLanguage('it')}>Italiano</Dropdown.Item>
            </Dropdown.Menu>
        </Dropdown>
    );
};

export default LanguageSwitcher;