import React from 'react';
import { format } from 'date-fns';
// import PropTypes from 'prop-types';

const DateTime = ({ dateToFormat }) => (
    <>
        <div>
            <div>{format(Date.parse(dateToFormat), 'MMM dd, yyyy')}</div>
        </div>
        <span style={{ fontSize: 12 }}>{format(Date.parse(dateToFormat), 'hh:mm a')}</span>
    </>
);

// DateTime.propTypes = {
//     dateToFormat: PropTypes.string.isRequired,
// };

export default DateTime;
