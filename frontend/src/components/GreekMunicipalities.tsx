// src/components/GreekMunicipalities.tsx

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Row, Col } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet';
import './GreekMunicipalities.css';

interface Municipality {
    name: string;
    slug: string;
    url: string;
}

interface Region {
    name: string;
    municipalities: Municipality[];
}

const GreekMunicipalities: React.FC = () => {
    const { t } = useTranslation();
    const [regions, setRegions] = useState<Region[]>([]);
    const [error, setError] = useState<string | null>(null);

    const fetchMunicipalities = () => {
        axios.get<Region[]>(`/api/geography/greece/municipalities/`)
            .then(response => {
                setRegions(response.data);
            })
            .catch(error => {
                setError(t('error_fetching_municipalities'));
                console.error('There was an error fetching the municipalities!', error);
            });
    };

    useEffect(() => {
        fetchMunicipalities();
    }, []);

    return (
        <Container>
            <Helmet>
                <title>{t('municipalities_of_greece')}</title>
            </Helmet>
            <h1>{t('municipalities_of_greece')}</h1>
            {error && <p className="error-message">{error}</p>}
            {regions.map(region => (
                <div key={region.name}>
                    <h2 className="region-title">{region.name}</h2>
                    <Row>
                        {region.municipalities.map(municipality => (
                            <Col key={municipality.slug} sm={12} md={6} lg={4}>
                                <div className="municipality">
                                    <h5>
                                        <a href={municipality.url || "#"}>{municipality.name}</a>
                                    </h5>
                                </div>
                            </Col>
                        ))}
                    </Row>
                </div>
            ))}
        </Container>
    );
};

export default GreekMunicipalities;