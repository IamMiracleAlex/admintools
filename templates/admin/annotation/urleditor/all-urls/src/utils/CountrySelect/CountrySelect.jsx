import React, { useState, useEffect } from 'react';
import axios from '../../axios';
import FormGroupSelect from '../FormGroup/FormGroupSelect/FormGroupSelect';

const CountrySelect = ({
    name,
    value,
    label,
    placeholder,
    isFilter,
    className,
    isMulti,
    onChange,
}) => {
    const [countryData, setCountryData] = useState();

    useEffect(() => {
        getCountryData();
    }, []);

    const getCountryData = async () => {
        try {
            const res = await axios.get('/annotation/countries/');

            if (res.status === 200) {
                const countryOptions = res.data.map(({ id, name }) => ({
                    value: id,
                    label: name,
                }));
                const filterOptions = [{ value: '', label: 'All' }, ...countryOptions];
                setCountryData(isFilter ? filterOptions : countryOptions);
            }
        } catch (error) {
            setCountryData([]);
        }
    };

    return (
        <FormGroupSelect
            label={label}
            name={name}
            placeholder={placeholder}
            options={countryData}
            value={value}
            isLoading={!countryData}
            isMulti={isMulti}
            onChange={onChange}
            className={className}
        />
    );
};

export default CountrySelect;
