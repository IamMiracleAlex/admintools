import React from 'react';
import {Table, Th, Td, Tr} from '@chakra-ui/react';

const HierarchyMapper = ({data, isHeader}) => {
    const Tag = isHeader ? Th : Td;
    
    return (
        <>
            {data.map((node, index) => (
            <Tag key={index}>{node !== "" ? node : "----"}</Tag>
            ))}
        </>
          
    )
}

export default HierarchyMapper;