import React from 'react';
import './Button.css';

const Button = ({ title, type = 'button', className, onClick, disabled, ...rest }) => {
    return (
        <button
            type={type}
            className={`btn ${className}`}
            onClick={onClick}
            disabled={disabled}
            {...rest}
        >
            {title}
        </button>
    );
};

export default Button;
