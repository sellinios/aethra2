import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

interface Division {
    slug: string;
    parent: Division | null;
}

interface Place {
    name: string;
    latitude: number;
    longitude: number;
    slug: string;
    admin_division: Division;
    url: string | null;
}

const useQuery = () => {
    return new URLSearchParams(useLocation().search);
};

const SearchResultsPage: React.FC = () => {
    const query = useQuery().get('query');
    const [places, setPlaces] = useState<Place[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (query) {
            const langCode = 'en'; // Change this dynamically based on user preference or context
            fetch(`/api/${langCode}/places-with-urls/?search=${query}`)
                .then(response => response.json())
                .then(data => {
                    if (Array.isArray(data)) {
                        setPlaces(data);
                    } else {
                        console.error('API response is not an array', data);
                        setError('Unexpected API response format');
                    }
                    setLoading(false);
                })
                .catch(error => {
                    console.error('Error fetching data', error);
                    setError(error.toString());
                    setLoading(false);
                });
        } else {
            setLoading(false);
        }
    }, [query]);

    if (loading) {
        return <div className="container mt-3">Loading...</div>;
    }

    if (error) {
        return <div className="container mt-3">Error: {error}</div>;
    }

    return (
        <div className="container mt-3">
            <h2>Search Results for "{query}"</h2>
            <ul className="list-group">
                {places.map(place => (
                    <li key={place.slug} className="list-group-item">
                        {place.url ? (
                            <a href={place.url} target="_blank" rel="noopener noreferrer">
                                {place.name}
                            </a>
                        ) : (
                            place.name
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default SearchResultsPage;