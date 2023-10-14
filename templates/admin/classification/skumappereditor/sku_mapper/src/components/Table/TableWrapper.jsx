import React from 'react';
import { useTable } from 'react-table';
import '../../utils/Table/Table.css';
import {
    Table,
    Th,
    Tbody,
    Tr,
    Td
} from '@chakra-ui/react'

const TableWrapper = ({ columns, data }) => {
   const tableInstance = useTable({columns,data});
   const  {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
    } = tableInstance

    return (
        <div className="table-responsive">
            <Table {...getTableProps()} className="table table-bordered">
                <Thead className="table__head">
                    {headerGroups.map((headerGroup) => (
                        <Tr {...headerGroup.getHeaderGroupProps()}>
                            {headerGroup.headers.map((column) => (
                                <Th {...column.getHeaderProps()}>{column.render('Header')}</Th>
                            ))}
                        </Tr>
                    ))}
                </Thead>
                <Tbody {...getTableBodyProps()} className="table__body">
                    {rows.map((row, i) => {
                        prepareRow(row);
                        return (
                            <Tr {...row.getRowProps()}>
                                {row.cells.map((cell) => {
                                    return <Td {...cell.getCellProps()}>{cell.render('Cell')}</Td>;
                                })}
                            </Tr>
                        );
                    })}
                </Tbody>
            </Table>
        </div>
    );
};

export default TableWrapper;
