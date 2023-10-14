import React from 'react';
import HierarchyMapper from './HierarchyMapper';
import {Td, Th} from '@chakra-ui/react';


const TableCell = ({ cellData, isHeader }) => {

    return (
        <>
            {Array.isArray(cellData) ? <HierarchyMapper data={cellData} isHeader={isHeader}/> : <Td>{cellData ? cellData : ""}</Td>}
        </>
    )
    
};

export default TableCell;
