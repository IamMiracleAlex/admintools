import React, {useContext} from 'react';
import {Thead, Tr, Th} from '@chakra-ui/react'
import {MapperContext} from '../Mapper'

const TableHeader = ({ headers }) => {

    const {skuMappers, setSelectedRows, selectedRows} = useContext(MapperContext);

    const onCheckBoxChange = (e) => {
        if (e.target.checked) {
            setSelectedRows(
                skuMappers.map((record) => ({
                    id: record.id,
                    checked: true,
                })),
            );
        } else {
            setSelectedRows([]);
        }
    }
    return (
        <Thead>
            <Tr>
                <Th>
                <input
                        type="checkbox"
                        id="exampleCheck1"
                        onChange={onCheckBoxChange}
                        style={{ marginRight: '14px' }}
                    />
                </Th>
               <Th>ID</Th>
               <Th>Product Name</Th>
               <Th>Manufacturer</Th>
               <Th>Description</Th>
               <Th colSpan="4">
                   Hierarchy Mapping
               </Th>
               <Th>Actions</Th>
            </Tr>
        </Thead>
    );
};

export default TableHeader;
