import React from 'react';
import './ErrorMessage.css';

const Error = ({ show, hide, message }) => {
    if (!show) return null;

    return (
        <div className="error-wrapper border border-danger mb-4">
            <span className="error__message">{message}</span>
            <button type="button" className="error__close-icon" onClick={hide}>
                <span>&times;</span>
            </button>
        </div>
    );
};

export default Error;
