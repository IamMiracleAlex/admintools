import React from 'react';
import { Input } from "@chakra-ui/react"
import PropTypes from 'prop-types';
import SearchIcon from '../../assets/svg/search-icon.svg'
import './index.css';

const Search = ({ placeholder, onChange, value }) => {
    return (
        <div className="custom-search-container">
            <Input
                className="custom-search-field"
                placeholder={placeholder}
                onChange={onChange}
                value={value}
            />
            <img src={SearchIcon} width="15px"/>
        </div>
    );
};

Search.propTypes = {
    placeholder: PropTypes.string,
    onChange: PropTypes.func,
};

export default Search;
