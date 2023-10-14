import React, { useState, useEffect } from 'react';
import ModalComponent from './ModalComponent';
import {Flex, Box, Button, Text} from '@chakra-ui/react';
import AsyncSelect from 'react-select/async';
import {fetchNodeSimpleList} from '../../services'
import { mapToHierarchy } from '../../services';

const HierarchyMappingModal = ({selectedRows, setAlert, refetchData}) => {
    const [show, setShow] = useState(false);
    const [loading, setLoading] = useState(false);
    const [selectedOption, setSelectedOption] = useState({})

    const fetchData = async (value="") => {
        const res = await fetchNodeSimpleList({q: value});
        if (res.status===200) {
            const options = res.data.map(({ id, title }) => ({
                value: id,
                label: title,
            }));
            return options;
        }
    }
    
    const mapToHierarchyHandler = async () => {
        setLoading(true)
        const skuIDs = selectedRows.map(({id}) => id);
        const payload = {node: selectedOption, sku_list: skuIDs}   
        try {
            const res = await mapToHierarchy(payload);
            if (res.status===200) {
                setLoading(false);
                setShow(false)
                refetchData();
                setAlert({
                    message: res.data,
                    status: "success",
                    show: true
                })
            }
        } catch(err) {
            setLoading(false)
            setShow(false)
            setAlert({
                message: err.message,
                status: "error",
                show: true
            })
        }
        
    }
  
    const onChangeHandler = (e) => {
        setSelectedOption(e);
    }

    const hideModal = () => {
        setShow(false);
    };

    return (
        <>
            <Button 
                onClick={() => setShow(true)} 
                className="btn-rad btn-wide" 
                colorScheme="blue" 
                mr="4">
                Map Selected SKUs to Hierarchy
            </Button>
            {show && (
                <ModalComponent
                    isOpen={show}
                    onClose={hideModal}
                    title="Hierarchy"
                    size="lg"
                >
                    <Box p="2">
                        {selectedRows?.length === 0 ?
                        (<Text mb="4" fontSize="13px">Select <strong>at least 1</strong> SKU to map to a given hierarchy node.</Text>)
                        :
                        (<Text mb="4" fontSize="13px">Map the <strong>{selectedRows?.length}</strong> selected SKUs to a given hierarchy node.</Text>)
                        }
                        <Box mb="4">
                            <AsyncSelect 
                                placeholder="Select Node..." 
                                cacheOptions 
                                defaultOptions
                                loadOptions={fetchData}
                                isDisabled={selectedRows?.length === 0} 
                                onChange={onChangeHandler}
                                style={{ marginBottom: "10px"}}
                            />
                        </Box>
                        <Flex className="justify-content-end">
                            <Button 
                                mr="3" 
                                className="btn-rad btn-wide" 
                                variant="outline" 
                                colorScheme="blue"
                                size="sm"
                                onClick={() => setShow(false)}
                            >Cancel</Button>
                            <Button 
                                className="btn-rad btn-wide" 
                                colorScheme="blue"
                                size="sm"
                                onClick={mapToHierarchyHandler}
                                isLoading={loading}
                                loadingText="Mapping ..."
                            >Save Mapped Hierarchy</Button>
                        </Flex>
                    </Box>

                </ModalComponent>
            )}
        </>
    );
};

export default HierarchyMappingModal;
