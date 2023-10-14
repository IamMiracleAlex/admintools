import React from 'react';
import TableCell from '../TableCell/TableCell';

const TableRow = ({ rowContent, inHeader }) => {
    const htmlTag = inHeader ? 'th' : 'td';

    return (
        <tr>
            {Object.values(rowContent).map((cellContent, i) => (
                <TableCell key={i} cellContent={cellContent} htmlTag={htmlTag} />
            ))}
        </tr>
    );
};

export default TableRow;
