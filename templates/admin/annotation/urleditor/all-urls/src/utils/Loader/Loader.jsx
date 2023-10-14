import React from 'react';
import { Spinner } from 'react-bootstrap';

const Loader = ({ size }) => {
    if (size === 'lg') {
        return (
            <Spinner
                animation="border"
                size="lg"
                role="status"
                variant="dark"
                className="custom-spinner-lg"
            />
        );
    }
    return (
        <>
            <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
            <span style={{ verticalAlign: 'middle' }}>Please Wait...</span>
        </>
    );
};

export default Loader;
