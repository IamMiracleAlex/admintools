import React, { useState, useEffect } from 'react';
import axios from '../../axios';
import FormGroupSelect from '../FormGroup/FormGroupSelect/FormGroupSelect';

const ClientSelect = ({
    name,
    value,
    label,
    className,
    placeholder,
    isFilter,
    isMulti,
    onChange,
}) => {
    const [clientData, setClientData] = useState();

    useEffect(() => {
        getClientData();
    }, []);

    const getClientData = async () => {
        try {
            const res = await axios.get('/annotation/clients/');

            if (res.status === 200) {
                const clientOptions = res.data.map(({ id, name }) => ({
                    value: id,
                    label: name,
                }));
                const filterOptions = [{ value: '', label: 'All' }, ...clientOptions];
                setClientData(isFilter ? filterOptions : clientOptions);
            }
        } catch (error) {
            setClientData([]);
        }
    };

    return (
        <FormGroupSelect
            label={label}
            name={name}
            className={className}
            placeholder={placeholder}
            options={clientData}
            value={value}
            isLoading={!clientData}
            isMulti={isMulti}
            onChange={onChange}
        />
    );
};

export default ClientSelect;
