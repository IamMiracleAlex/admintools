import React, { useState } from 'react';
import ModalComponent from './ModalComponent';
import {Flex, Box, Button, Text, Input} from '@chakra-ui/react';
import { createManufacturer } from '../../services';
import CustomAlert from './CustomAlert';

const NewManufacturer = ({className="btn-rad btn-wide", setAlert, title, refetchData}) => {
    const [isVisible, setIsVisible] = useState(false);
    const [showError, setShowError] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState({
        message: "",
        title: ""
    })
    const [name, setName] = useState("");

    const onSubmitHandler = async () => {
        setLoading(true)  
        try {
            const payload = {name} 
            const res = await createManufacturer(payload);
            if (res.status === 201) {
                setLoading(false);
                refetchData()
                setAlert({
                    message: res.data,
                    status: "success",
                    show: true
                })
                setIsVisible(false)
            }
        } catch (err) { 
            setLoading(false);
            setShowError(true);
            setError({
                message: err.message,
            })        
        }
    }
  
    const onChangeHandler = ({target}) => {
        setName(target.value);
    }

    const hideModal = () => {
        setIsVisible(false);
        setShowError(false);
    };



    return (
        <>
            <Button 
                onClick={() => setIsVisible(true)} 
                className={className} 
                colorScheme="blue" 
                style={{marginLeft: "10px"}}
                mr="4">
                {title}
            </Button>
            {isVisible && (
                <ModalComponent
                    isOpen={isVisible}
                    onClose={hideModal}
                    title="Add Manufacturer"
                    size="lg"
                >
                    <Box p="2">
                        <CustomAlert 
                            open={showError} 
                            message={error.message}
                            close={() => setShowError(false)}
                            status="error" />
                        <Text mb="4" fontSize="13px">Add a <strong>New Manufacturer</strong></Text>
                        <Box mb="4">
                            <Input 
                                placeholder="Manufacturer name here..." 
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
                                onClick={() => setIsVisible(false)}
                            >Cancel</Button>
                            <Button 
                                className="btn-rad btn-wide" 
                                colorScheme="blue"
                                size="sm"
                                onClick={onSubmitHandler}
                                isLoading={loading}
                                loadingText="Please wait ..."
                            >Submit</Button>
                        </Flex>
                    </Box>

                </ModalComponent>
            )}
        </>
    );
};

export default NewManufacturer;
