import React from 'react';
import './Pill.css';

export const Pill = ({ status = '' }) => {
    return (
        <span className={`badge badge-pill badge-${status}`}>
            <span className={`status-circle circle-${status}`}></span>
            <span>{status}</span>
        </span>
    );
};
