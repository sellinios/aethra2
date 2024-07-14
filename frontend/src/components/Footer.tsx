import React from 'react';
import { Container } from 'react-bootstrap';

const Footer = () => {
    const currentYear = new Date().getFullYear();
    return (
        <footer className="bg-dark text-white mt-5 p-3 text-center">
            <Container>
                <p>© {currentYear} Kairos. All rights reserved.</p>
            </Container>
        </footer>
    );
};

export default Footer;