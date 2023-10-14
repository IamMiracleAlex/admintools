import React from 'react';
import { FormControl } from 'react-bootstrap';
import SearchIcon from '../../../assets/svg/search-icon.svg';
import PropTypes from 'prop-types';

import './FormGroupSearch.css';

const FormGroupSearch = ({ placeholder, onChange, value }) => {
    return (
        <div className="custom-search-container">
            <FormControl
                className="custom-search-field"
                placeholder={placeholder}
                onChange={onChange}
                value={value}
            />
            <SearchIcon />
        </div>
    );
};

FormGroupSearch.propTypes = {
    placeholder: PropTypes.string,
    onChange: PropTypes.func,
};

export default FormGroupSearch;
