import React from 'react';
import { format } from 'date-fns';
import { Pill } from '../Pill/Pill';

export const StatusColumn = ({ status = '', date = '' }) => {
    return (
        <div>
            <Pill status={status} />
            <div>Last Updated: {format(Date.parse(date), 'dd/MMM/yyyy hh:mm:ss')}</div>
        </div>
    );
};
