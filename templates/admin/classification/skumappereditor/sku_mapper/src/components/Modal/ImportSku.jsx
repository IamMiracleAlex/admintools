import React, { useState, useContext } from 'react';
// import axios from '../axios';
// import Button from '../utils/Button/Button';
// import Modal from '../utils/Modal/Modal';
// import Loader from '../utils/Loader/Loader';
import ModalComponent from './ModalComponent';
import {Input, Box, Button, Text, Flex} from '@chakra-ui/react';
import {importSKU} from '../../services';
import CustomAlert from './CustomAlert';

const ImportSkuMapping = ({setAlert, refetchData }) => {
    const [show, setShow] = useState(false);
    const [showError, setShowError] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState({
        message: "",
        status: ""
    })

    const hideModal = () => {
        setShow(false);
        setShowError(false);
        setLoading(false)
        setLoading(false)
    };

    const onFileChange = (e) => {
        // Update the state selectedFile state
        setSelectedFile(e.target.files[0]);
      };
    
      const onFileUpload = async () => {
          setLoading(!loading)
        // Create an object of formData
        const formData = new FormData();
        // Update the formData object
        formData.append(
            "file",
            selectedFile,
            selectedFile.name
        );
        // send request to the backend api
        try {
            const response = await importSKU(formData)
            if (response.status === 201) {
                hideModal();
                refetchData()
                setAlert({
                    message: response.data.message,
                    status: "success",
                    show: true
                })
            }
        } catch(err) {
            setLoading(false)
            setShowError(true)
            setError({
                message: err.message,
                status: "error"
            })
        }
      }

    return (
        <>
            <Button 
                onClick={() => setShow(true)} 
                className="btn-rad btn-wide" 
                variant="outline" 
                colorScheme="blue" 
                mr="4">
                Import SKU File
            </Button>
            {show && (
                <ModalComponent
                    isOpen={show}
                    onClose={hideModal}
                    title="Import SKU File"
                    size="lg"
                >
                    <Box p="2">
                        <CustomAlert 
                            open={showError}
                            message={error.message}
                            status={error.status}
                            close={() => setShowError(false)} 
                        />
                        <Text fontSize="13px" mb="6">
                            Kindly make sure you files (SKUs) include SKU IDs, description, product name,
                            variation, sales quantity, sales values and last sales values
                        </Text>
                        <Input type="file" onChange={onFileChange}/>
                    </Box>
                    <Flex className="justify-content-end">
                            <Button 
                                mr="2" 
                                className="btn-rad btn-wide" 
                                variant="outline" 
                                colorScheme="blue"
                                size="sm"
                                onClick={() => setShow(false)}
                            >Cancel</Button>
                            <Button 
                                size="sm" 
                                className="btn-rad btn-wide" 
                                colorScheme="blue"
                                onClick={onFileUpload}
                                isLoading={loading}
                                loadingText="Uploading..."
                            >Import</Button>
                        </Flex>
                </ModalComponent>
            )}
        </>
    );
};

export default ImportSkuMapping;
