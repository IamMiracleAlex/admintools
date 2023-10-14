import React from 'react';
import {
    Alert,
    AlertIcon,
    AlertTitle,
    AlertDescription,
    CloseButton
  } from "@chakra-ui/react"

const CustomAlert = ({open, close, message, status="info" }) => {


    if (!open) return null;
    
    return (
        <>
            <Alert status={status} variant="left-accent">
                <AlertIcon />
                <AlertDescription>{message}</AlertDescription>
                <CloseButton position="absolute" right="4px" top="4px" size="sm" onClick={close} />
            </Alert>
        </>       
    )
}

export default CustomAlert;