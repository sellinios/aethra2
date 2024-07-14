import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import LocationFinder from './LocationFinder';

const UpperHeader: React.FC = () => {
    return (
        <Container fluid className="bg-light py-2">
            <Row>
                <Col className="text-center">
                    <LocationFinder />
                </Col>
            </Row>
        </Container>
    );
};

export default UpperHeader;