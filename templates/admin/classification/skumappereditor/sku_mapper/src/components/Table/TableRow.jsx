import React, {useContext} from 'react';
import TableCell from './TableCell';
import {Tr, Td} from '@chakra-ui/react';
import Actions from './Actions';
import {MapperContext}  from '../Mapper';


const TableRow = ({ rowObject,setAlert, isHeader, refetchData }) => {
    const {id, client, ...tableData} = rowObject;
    const {setSelectedRows, selectedRows} = useContext(MapperContext)

    const onCheckHandler = (e) => {
        if (!e.target.checked) {
            setSelectedRows(selectedRows.filter((e) => e.id !== id));
        } else {
            const newObj = {
                id: id,
                checked: e.target.checked,
            };
            setSelectedRows([...selectedRows, newObj]);
        }
    }

    return (
        <Tr>
            <Td>
                <input
                    type="checkbox" 
                    checked={selectedRows.find((e) => e.id === id)?.checked || false}
                    onChange={onCheckHandler}  
                />
            </Td>
            {Object.values(tableData).map((cellContent, i) => (
                <TableCell key={i} cellData={cellContent} isHeader={isHeader} />
            ))}
            <Td style={{float: "right"}}>
                <Actions setAlert={setAlert} refetchData={refetchData} record={rowObject} />
            </Td>
        </Tr>
    );
};

export default TableRow;
