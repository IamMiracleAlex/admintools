import React from 'react';
import { FormControl } from 'react-bootstrap';
import SearchIcon from '../../assets/svg/search-icon.svg';

import './FormGroupSearch.css';

export const FormGroupSearch = ({ onChange, value }) => {
    return (
        <div className="custom-search-container">
            <FormControl
                className="custom-search-field"
                placeholder="Search"
                onChange={onChange}
                value={value}
            />
            <SearchIcon />
        </div>
    );
};
