// src/components/Search.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Search.css';

const Search: React.FC = () => {
    const [query, setQuery] = useState('');
    const navigate = useNavigate();

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        navigate(`/search?query=${query}`);
    };

    return (
        <div className="container mt-3 search-container">
            <form className="search-form" onSubmit={handleSearch}>
                <input
                    type="text"
                    className="form-control search-input"
                    placeholder="Search..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button type="submit" className="btn btn-primary search-button">Search</button>
            </form>
        </div>
    );
};

export default Search;