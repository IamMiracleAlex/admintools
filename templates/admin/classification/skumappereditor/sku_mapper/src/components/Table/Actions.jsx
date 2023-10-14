import React from 'react';
import {Flex} from '@chakra-ui/react';
import {
    CreateSingleSKU, 
    DeleteModal, 
    EditMapper, 
    ViewMappedSku
} from '../Modal/AllActionModal'

const Actions = ({record=null, setAlert, refetchData}) => {

    const isMapped = () => {
        return Object.values(record?.node_hierarchy).find(item => item !== "")
    }

    return (
        <>
        <Flex>
            <ViewMappedSku sku={record} />
            <EditMapper colorScheme="blue" sku={record} />
            <DeleteModal setAlert={setAlert} refetchData={refetchData} colorScheme="red" sku={record} />
            {!isMapped() ? <CreateSingleSKU setAlert={setAlert} refetchData={refetchData} colorScheme="green" sku={record}/> : null}
        </Flex>
        </>
    )
}

export default Actions;