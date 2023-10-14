import React, { useState, useEffect } from 'react';
// import axios from '../axios';
// import Button from '../utils/Button/Button';
// import Modal from '../utils/Modal/Modal';
// import Loader from '../utils/Loader/Loader';
import ModalComponent from './ModalComponent';
import {Flex, Box, Button, Text} from '@chakra-ui/react';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import {
    FormControl,
    FormLabel,
    HStack,
    Input,
    Textarea,
  } from "@chakra-ui/react";
  import {
    NumberInput,
    NumberInputField,
  } from "@chakra-ui/react"
import {BsPlus} from 'react-icons/bs';
import AsyncSelect from 'react-select/async';
import { fetchManufacturers, fetchNodeSimpleList, submitSkuData } from '../../services';
import NewManufacturer from './NewManufacturer';
import CustomAlert from './CustomAlert';


const NewMapping = ({clientID, setAlert, refetchData}) => {
    const [show, setShow] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState({
        message: "",
        status: "",
        showError: false
    })
    const [state, setState] = useState({
        client: clientID,
        product_name: "",
        sku_id: "",
        manufacturer: null,
        description: "",
        hierarchy_mapping: null,
        product_name_variation: "",
        last_sale: null,
        sales_value: 0,
        sales_quality: 0,
    })

    const fetchManufacturerData = async (value="") => {
        const res = await fetchManufacturers({q: value});
        if (res.status===200) {
            const options = res.data.results.map(({ id, name }) => ({
                value: id,
                label: name,
                name: "manufacturer"
            }));
            return options;
        }
    }

    const fetchNodeData = async (value="") => {
        const res = await fetchNodeSimpleList({q: value});
        if (res.status===200) {
            const options = res.data.map(({ id, title }) => ({
                value: id,
                label: title,
                name: "hierarchy_mapping"
            }));
            return options;
        }
    }
    
    const submitHandler = async () => {
        setLoading(true)
        try {
            const res = await submitSkuData(state);
            if (res.status === 201) {
                setLoading(false);
                refetchData()
                setShow(false);
                setAlert({
                    message: "SKU successfully added",
                    status: "success",
                    show: true
                })
            } else {
                setLoading(false)
                setShow(false)
            }
        } catch(err) {
            setError({
                message: err.message,
                status: "error",
                showError: true
            })
        }
    }
    const hideModal = () => {
        setShow(false);
        setError({...error, showError: false});
    };

    const onSelectChangeHandler = (e) => {
        setState({...state, [e.name]: e.value});
    }

    const onInputChangeHandler = ({target}) => {
        setState({
            ...state,
            [target.name]: target.value,
        })
    }

    useEffect(() => {
        fetchManufacturerData();
    }, [])

    return (
        <>
            <Button 
                colorScheme="blue" 
                className="btn-rad" 
                style={{marginRight: "15px"}}
                onClick={() => setShow(true)} 
            >
                <BsPlus size="1.4em"/>
            </Button>
            {show && (
                <ModalComponent
                    isOpen={show}
                    onClose={hideModal}
                    title="Add SKU"
                    size="xl"
                >
                    <Box p="2">
                        <Box mb="4">
                            <CustomAlert 
                                open={error.showError}
                                message={error.message}
                                status={error.status}
                                close={() => setError({...error, showError:false})} 
                            />
                            <HStack mb="3" size="sm">
                                <FormControl>
                                    <FormLabel fontSize="sm" htmlFor="name">Product Name *</FormLabel>
                                    <Input 
                                        onChange={onInputChangeHandler} 
                                        placeholder="Product Name"
                                        required
                                        name="product_name" />
                                </FormControl>
                                <FormControl>
                                    <FormLabel fontSize="sm" htmlFor="name">SKU ID *</FormLabel>
                                    <Input 
                                        placeholder="SKU ID goes here..."
                                        onChange={onInputChangeHandler}
                                        required
                                        name="sku_id" />
                                </FormControl>
                            </HStack>
                            <Box mb="3">
                                <FormControl mb="3">
                                    <FormLabel mb="0" fontSize="sm" htmlFor="name">Manufacturer *</FormLabel>
                                    <small>You can add a new record and type the name below to search for it</small>
                                    <Flex w="100%">
                                        <Box w="90%">
                                            <AsyncSelect 
                                                placeholder="Select or search manufacturer..." 
                                                required
                                                cacheOptions 
                                                defaultOptions
                                                loadOptions={fetchManufacturerData}
                                                onChange={onSelectChangeHandler}
                                                style={{ marginBottom: "10px", width: "90%"}}
                                            />
                                        </Box>
                                        <NewManufacturer setAlert={() => {}} className="btn-rad" title="+" refetchData={fetchManufacturerData} />
                                    </Flex>
                                </FormControl>
                                <FormControl mb="3">
                                    <FormLabel fontSize="sm" htmlFor="name">Description</FormLabel>
                                    <Textarea 
                                        placeholder="Say something about this product"
                                        onChange={onInputChangeHandler}
                                        name="description" />
                                </FormControl>
                                <FormControl mb="3">
                                    <FormLabel fontSize="sm" htmlFor="name">Hierarchy Node</FormLabel>
                                    <AsyncSelect 
                                        placeholder="Select or search hierarchy..." 
                                        cacheOptions 
                                        defaultOptions
                                        loadOptions={fetchNodeData}
                                        onChange={onSelectChangeHandler}
                                        style={{ marginBottom: "10px"}}
                                    />
                                </FormControl>
                                <FormControl mb="3">
                                    <FormLabel fontSize="sm" htmlFor="name">Product Name Variation</FormLabel>
                                    <Input 
                                        onChange={onInputChangeHandler} 
                                        placeholder="Product name variation"
                                        name="product_name_variation" 
                                    />
                                </FormControl>
                                <FormControl mb="3">
                                    <FormLabel fontSize="sm" htmlFor="name">Sales Quantity</FormLabel>
                                    <NumberInput step={1} defaultValue={0} min={0}>
                                        <NumberInputField
                                            onChange={onInputChangeHandler} 
                                            name="sales_quality"/>
                                    </NumberInput>
                                </FormControl>
                                <FormControl mb="3">
                                    <FormLabel fontSize="sm" htmlFor="name">Sales Value</FormLabel>
                                    <NumberInput step={1} defaultValue={0}>
                                        <NumberInputField
                                            onChange={onInputChangeHandler}
                                            name="sales_value" />
                                    </NumberInput>
                                </FormControl>
                                <FormControl mb="3">
                                    <FormLabel fontSize="sm" htmlFor="name">Last Sale</FormLabel>
                                    <DatePicker 
                                        style={{borderColor: "#C7CADD"}}
                                        name="last_sale"
                                        isClearable
                                        onChange={(date) => setState({...state, last_sale: date})} 
                                        selected={state.last_sale}
                                    />
                                </FormControl>
                            </Box>

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
                                disabled={!(state.product_name && state.sku_id && state.manufacturer)}
                                onClick={submitHandler}
                                loadingText="Saving..."
                                isLoading={loading}
                            >Save</Button>
                        </Flex>
                    </Box>

                </ModalComponent>
            )}
        </>
    );
};

export default NewMapping;
