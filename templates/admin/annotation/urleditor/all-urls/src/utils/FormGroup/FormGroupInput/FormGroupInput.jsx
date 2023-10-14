import React from 'react';
import './FormGroupInput.css';

const FormGroupInput = ({
    label,
    type = 'text',
    id,
    name,
    placeholder = '',
    value,
    className = '',
    readonly,
    error,
    onChange,
    required,
    ...rest
}) => {
    return (
        <div className={`form-group ${className}`}>
            {label && (
                <label htmlFor={id} className="form-group__label">
                    {label}
                    {required && <span className="text-danger pl-1">*</span>}
                </label>
            )}

            <input
                type={type}
                id={id}
                name={name}
                placeholder={placeholder}
                value={value}
                className="form-group__input"
                // readOnly={readonly}
                // autoComplete="off"
                // data-error={Boolean(error)}
                required={required}
                onChange={onChange}
                {...rest}
            />

            {/* {typeof error === 'string' && (
                <small className="form-group__error-text text-danger">{error}</small>
            )} */}
        </div>
    );
};

export default FormGroupInput;
