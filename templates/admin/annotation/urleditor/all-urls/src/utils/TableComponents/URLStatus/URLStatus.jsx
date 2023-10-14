import React from 'react';
import PropTypes from 'prop-types';

const URLStatus = ({ status = '' }) => {
    return (
        <div className="d-flex align-items-center justify-content-between">
            <span className="text-capitalize">{status}</span>
            <span className={`url-status-circle ${status}`}></span>
        </div>
    );
};

URLStatus.propTypes = {
    status: PropTypes.string.isRequired,
};

export default URLStatus;
