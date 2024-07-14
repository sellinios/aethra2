// src/components/Header.tsx
import React from 'react';
import { Navbar, Container, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from './LanguageSwitcher';
import Logo from './Logo';

const Header: React.FC = () => {
    const { t } = useTranslation();

    return (
        <header className="header">
            <Navbar bg="dark" variant="dark" expand="lg">
                <Container>
                    <Navbar.Brand href="/" className="navbar-brand">
                        <Logo />
                    </Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="ml-auto">
                            <Nav.Item>
                                <Nav.Link as={Link} to="/">{t('home')}</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link as={Link} to="/about">{t('about')}</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link as={Link} to="/contact">{t('contact')}</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link as={Link} to="/geography/greece/municipalities">{t('municipalities')}</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link as={Link} to="/login">{t('login')}</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link as={Link} to="/register">{t('register')}</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <LanguageSwitcher />
                            </Nav.Item>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </header>
    );
};

export default Header;