import React, { useState, useContext } from 'react';
import ModalComponent from './ModalComponent';
import AsyncSelect from 'react-select/async';
// import axios from '../axios';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import {
    Flex, 
    Box, 
    Button, 
    Text,
    FormControl,
    Select,
    FormLabel,
    HStack,
    Input,
    Image,
    Center,
    Textarea,
    Table,
    Tbody,
    Tr, Th,Td
} from "@chakra-ui/react";
import {
    NumberInput,
    NumberInputField,
    NumberInputStepper,
    NumberIncrementStepper,
    NumberDecrementStepper,
} from "@chakra-ui/react";
import {
    AlertDialog,
    AlertDialogBody,
    AlertDialogFooter,
    AlertDialogContent,
    AlertDialogOverlay,
  } from "@chakra-ui/react";
import {AiOutlineEdit} from 'react-icons/ai';
import {RiDeleteBinLine} from 'react-icons/ri';
import {GiCheckboxTree} from 'react-icons/gi';
import {BsEye} from 'react-icons/bs';
import deleteImage from '../../assets/svg/delete.svg';
import { deleteSKU } from '../../services';
import { MapperContext } from '../Mapper';
import {fetchNodeSimpleList, mapToHierarchy} from '../../services'



export const CreateSingleSKU = ({colorScheme, setAlert, refetchData, sku=null}) => {
    const [show, setShow] = useState(false);
    const [showError, setShowError] = useState(false);
    const [loading, setLoading] = useState(false);
    const [selectedOption, setSelectedOption] = useState({})
    const {selectedRows, setSelectedRows} = useContext(MapperContext);

    const mapToHierarchyHandler = async () => {
        setLoading(true)
        setSelectedRows([])
        const skuIDs =  [sku.id];
        const payload = {node: selectedOption, sku_list: skuIDs}   
        try{
            const res = await mapToHierarchy(payload);
            if (res.status===200) {
                setLoading(false);
                setShow(false)
                refetchData()
                setAlert({
                message: res.data,
                status: "success",
                show: true
                })
            }
        }catch(err) {
            setLoading(false);
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

    const hideModal = () => {
        setShow(false);
        setShowError(false);
    };

    return (
        <>
            <Button 
                colorScheme={colorScheme} 
                mr="1.5" 
                size="sm"
                onClick={() => setShow(true)} 
                >
                <GiCheckboxTree size="1.4em"/>
            </Button>
            {show && (
                <ModalComponent
                    isOpen={show}
                    onClose={hideModal}
                    title="Hierarchy"
                    size="lg"
                >
                    <Box p="2">
                        <Text mb="4" fontSize="13px">Mapping <strong>{sku.product_name}</strong> to a Hierarchy</Text>
                        <Box mb="4">
                            <AsyncSelect 
                                placeholder="Select Node..." 
                                cacheOptions 
                                defaultOptions
                                loadOptions={fetchData}
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


export const DeleteModal = ({colorScheme, setAlert, refetchData, sku=null}) => {
    const [show, setShow] = useState(false);
    const [loading, setLoading] = useState(false);
    const cancelRef = React.useRef()

    const hideModal = () => {
        setShow(false);
    };

    const deleteHandler = async () => {
        try {
            setLoading(true);
            const res = await deleteSKU(sku.id);
            if (res.status===200) {
                setLoading(false)
                hideModal();
                refetchData();
                setAlert({
                    message: res.data.message,
                    status: "info",
                    show: true
                })
            }
        } catch(err) {
            setAlert({
                message: err.message,
                status: "error",
                show: true
            })
        } finally {
            setLoading(false);
            hideModal();

        }
    }

    return (
        <>
            <Button 
                onClick={() => setShow(true)} 
                colorScheme={colorScheme}
                size="sm"
                mr="1.5">
                <RiDeleteBinLine  size="1.2em"/>
            </Button>
            <AlertDialog
                isOpen={show}
                leastDestructiveRef={cancelRef}
                onClose={hideModal}
            >
                <AlertDialogOverlay>
                <AlertDialogContent>
                    <AlertDialogBody>
                        <Center m="7">
                            <Image src={deleteImage} size="lg"/>
                        </Center>
                        <Box style={{textAlign: "center"}}>
                            <Text>Are you sure you want to remove <strong>{sku?.product_name} with SKU ID: {sku.sku_id}</strong>? 
                            <br></br>You can't undo this action afterwards.</Text>
                        </Box>
                    </AlertDialogBody>

                    <Center>
                        <AlertDialogFooter mb="4" style={{textAlign: "center"}}>
                            <Button 
                                variant="outline" 
                                className="btn-rad btn-wide" 
                                ref={cancelRef}
                                colorScheme="blue"
                                onClick={hideModal}
                            >
                            Cancel
                            </Button>
                            <Button 
                                className="btn-rad btn-wide" 
                                colorScheme="red" 
                                onClick={deleteHandler} 
                                ml={3}
                                isLoading={loading}
                                loadingText="Please wait...">
                                Remove
                            </Button>
                        </AlertDialogFooter>
                    </Center>
                </AlertDialogContent>
                </AlertDialogOverlay>
            </AlertDialog>
        </>
    );
};

export const EditMapper = ({colorScheme, sku=null}) => {
    const [show, setShow] = useState(false);
    const [showError, setShowError] = useState(false);
    const [startDate, setStartDate] = useState(new Date());
    
    const colourOptions = [
        { value: 'chocolate', label: 'Chocolate' },
        { value: 'strawberry', label: 'Strawberry' },
        { value: 'vanilla', label: 'Vanilla' }
      ]

    const filterColors = (inputValue) => {
        return colourOptions.filter(i =>
          i.label.toLowerCase().includes(inputValue.toLowerCase())
        );
      };
      
      const promiseOptions = inputValue =>
        new Promise(resolve => {
          setTimeout(() => {
            resolve(filterColors(inputValue));
          }, 1000);
        });

    const hideModal = () => {
        setShow(false);
        setShowError(false);
    };

    return (
        <>
            <Button 
                colorScheme={colorScheme} 
                mr="1.5" 
                size="sm"
                onClick={() => setShow(true)} 
                >
                <AiOutlineEdit size="1.4em"/>
            </Button>
            {show && (
                <ModalComponent
                    isOpen={show}
                    onClose={hideModal}
                    title="Edit SKU"
                    size="xl"
                >
                    <Box p="2">
                        <Box mb="4">
                            <HStack mb="3" size="sm">
                                <FormControl>
                                    <FormLabel fontSize="sm" htmlFor="name">Product Name</FormLabel>
                                    <Input placeholder="Product Name" value={sku.product_name} />
                                </FormControl>
                                <FormControl>
                                    <FormLabel fontSize="sm" htmlFor="name">SKU ID</FormLabel>
                                    <Input placeholder="SKU ID goes here..." value={sku.sku_id} />
                                </FormControl>
                            </HStack>
                            <Box mb="3">
                                <FormControl mb="3">
                                    <FormLabel fontSize="sm" htmlFor="name">Manufacturer</FormLabel>
                                    <Select placeholder="Select Manufacturer..." value={sku.manufacturer}>
                                        <option value="option1">Option 1</option>
                                        <option value="option2">Option 2</option>
                                        <option value="option3">Option 3</option>
                                    </Select>
                                </FormControl>
                                <FormControl mb="3">
                                    <FormLabel fontSize="sm" htmlFor="name">Description</FormLabel>
                                    <Textarea placeholder="Say something about this product" value={sku.description} />
                                </FormControl>
                                <FormControl mb="3">
                                    <FormLabel fontSize="sm" htmlFor="name">Hierarchy Node</FormLabel>
                                    <AsyncSelect 
                                        placeholder="Select Node..." 
                                        cacheOptions 
                                        defaultOptions 
                                        loadOptions={promiseOptions} 
                                        value={sku.node}
                                    />
                                </FormControl>
                                <FormControl mb="3">
                                    <FormLabel fontSize="sm" htmlFor="name">Product Name Variation</FormLabel>
                                    <Input placeholder="" value={sku.product_name_variation} />
                                </FormControl>
                                <FormControl mb="3">
                                    <FormLabel fontSize="sm" htmlFor="name">Sales Quantity</FormLabel>
                                    <NumberInput step={1} value={sku.sales_quantity} min={0}>
                                        <NumberInputField />
                                        <NumberInputStepper>
                                            <NumberIncrementStepper />
                                            <NumberDecrementStepper />
                                        </NumberInputStepper>
                                    </NumberInput>
                                </FormControl>
                                <FormControl mb="3">
                                    <FormLabel fontSize="sm" htmlFor="name">Sales Value</FormLabel>
                                    <NumberInput step={1} defaultValue={0}>
                                        <NumberInputField />
                                        <NumberInputStepper>
                                            <NumberIncrementStepper />
                                            <NumberDecrementStepper />
                                        </NumberInputStepper>
                                    </NumberInput>
                                </FormControl>
                                <FormControl mb="3">
                                    <FormLabel fontSize="sm" htmlFor="name">Last Sale</FormLabel>
                                    <DatePicker 
                                        style={{borderColor: "#C7CADD"}}
                                        selected={startDate}
                                        isClearable
                                        onChange={(date) => setStartDate(date)} 
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
                            >Save</Button>
                        </Flex>
                    </Box>

                </ModalComponent>
            )}
        </>
    );
};

export const ViewMappedSku = ({sku=null}) => {
    const [show, setShow] = useState(false);
    const [showError, setShowError] = useState(false);
    
    const hideModal = () => {
        setShow(false);
        setShowError(false);
    };

    return (
        <>
            <Button 
                variant="outline" 
                mr="1.5" 
                size="sm"
                onClick={() => setShow(true)} 
                >
                <BsEye size="1.4em"/>
            </Button>
            {show && (
                <ModalComponent
                    isOpen={show}
                    onClose={hideModal}
                    title={sku?.product_name}
                    size="xl"
                >
                    <Box p="2">
                        <Box mb="4">
                            <Table variant="simple">
                                <Tbody>
                                    <Tr>
                                        <Th>SKU ID</Th>
                                        <Td>{sku?.sku_id}</Td>
                                    </Tr>
                                    <Tr>
                                        <Th>Category</Th>
                                        {sku?.node_hierarchy ? (
                                        <Td>{sku?.node_hierarchy.map((text) => text !== null ? text.toUpperCase():"None").join(">>")}</Td>
                                        ):null}
                                    </Tr>
                                    <Tr>
                                        <Th>Mapped To</Th>
                                        {sku.node_hierarchy ? (
                                        <Td style={{width: "70%"}}>
                                            {sku?.node_hierarchy.map((text) => (<small className="inner-td">{text ? text.toUpperCase() : " -- "} </small>))}
                                        </Td>):null}
                                    </Tr>
                                    <Tr>
                                        <Th>Product Name Variation</Th>
                                        <Td>{sku?.product_name_variation}</Td>
                                    </Tr>
                                    <Tr>
                                        <Th>Sales Quantity</Th>
                                        <Td isNumeric>{sku?.sales_quantity}</Td>
                                    </Tr>
                                    <Tr>
                                        <Th>Sales Value</Th>
                                        <Td>{sku?.sales_value}</Td>
                                    </Tr>
                                    <Tr>
                                        <Th>Last Sales</Th>
                                        <Td>{sku?.last_sales}</Td>
                                    </Tr>
                                </Tbody>
                            </Table>
                        </Box>
                        <Flex className="justify-content-end">
                            <Button 
                                mr="3" 
                                className="btn-rad btn-wide" 
                                colorScheme="blue"
                                size="sm"
                                onClick={() => setShow(false)}
                            >Done</Button>
                        </Flex>
                    </Box>

                </ModalComponent>
            )}
        </>
    );
};