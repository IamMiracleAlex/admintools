import React from 'react';
import {CheckBox} from '@chakra-ui/react'


const TableCheckBox = ({ onChange, checked }) => {
    return (
        <>
            <CheckBox
                id="exampleCheck1"
                onChange={onChange}
                style={{ marginRight: '10px' }}
                isChecked={checked}
            />
        </>
    );
};

export default TableCheckBox;
