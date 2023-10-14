import React from 'react';
import TableRow from '../TableRow/TableRow';

const TableHead = ({ headers }) => {
    return (
        <thead className="table__head">
            <TableRow rowContent={headers} inHeader={true} />
        </thead>
    );
};

export default TableHead;
