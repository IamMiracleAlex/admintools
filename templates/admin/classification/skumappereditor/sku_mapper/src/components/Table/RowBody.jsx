import React from 'react';
import TableRow from './TableRow';
import {Tbody} from '@chakra-ui/react';

const TableBody = ({ dataSource, setAlert, selectedRows, refetchData }) => {
    
    return (
        <Tbody className="table__body">
            {dataSource.map((data, i) => (
                <TableRow 
                    setAlert={setAlert} 
                    refetchData={refetchData} 
                    key={i} 
                    rowObject={data} 
                    selectedRow={selectedRows} 
                    isHeader={false} 
                />
            ))}
        </Tbody>
    );
};

export default TableBody;
