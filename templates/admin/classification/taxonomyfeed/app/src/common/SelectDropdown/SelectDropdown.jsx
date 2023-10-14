import React from 'react';
import Select from 'react-select';
import './SelectDropdown.css';

export const SelectDropdown = ({
    label,
    id,
    name,
    placeholder,
    isMulti,
    options,
    value,
    defaultValue,
    error,
    className = '',
    onChange,
    required,
    ...rest
}) => {
    return (
        <div className="form-group">
            {label && (
                <label htmlFor={id} className="form-group__label">
                    {label}
                    {required && <span className="text-danger pl-1">*</span>}
                </label>
            )}

            <div
                className={`custom-select-container select-wrapper ${className} ${
                    isMulti ? '--is-multi' : ''
                }`}
                data-error={Boolean(error)}
            >
                {error && <span className="required-select">This field is required</span>}
                <Select
                    inputId={id}
                    name={name}
                    placeholder={placeholder}
                    options={options}
                    value={value}
                    isMulti={isMulti}
                    required={required}
                    defaultValue={defaultValue}
                    className="custom-select-container"
                    classNamePrefix="custom-react-select"
                    onChange={onChange}
                    {...rest}
                />
            </div>
        </div>
    );
};
