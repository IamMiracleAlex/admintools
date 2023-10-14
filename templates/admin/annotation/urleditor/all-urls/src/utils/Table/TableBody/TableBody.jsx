import React from 'react';
import TableRow from '../TableRow/TableRow';

const TableBody = ({ dataSource }) => {
    return (
        <tbody className="table__body">
            {dataSource.map((data, i) => (
                <TableRow key={i} rowContent={data} />
            ))}
        </tbody>
    );
};

export default TableBody;
