import React from 'react';
import PropTypes from 'prop-types';

const URLPriority = ({ priority }) => {
    let text = '';
    switch (priority) {
        case (priority = 1):
            text = 'High';
            break;
        case (priority = 2):
            text = 'Medium';
            break;
        case (priority = 3):
            text = 'Low';
            break;
        default:
            break;
    }
    return text;
};

URLPriority.propTypes = {
    priority: PropTypes.number.isRequired,
};

export default URLPriority;
