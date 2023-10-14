import React from 'react';

const TableCell = ({ cellContent, htmlTag }) => {
    return React.createElement(htmlTag, null, cellContent);
};

export default TableCell;
