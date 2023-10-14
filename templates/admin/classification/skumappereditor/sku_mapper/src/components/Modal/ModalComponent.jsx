import React from 'react';
import {
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton,
    Button
  } from "@chakra-ui/react";

const ModalComponent = ({ isOpen, onClose, size, title, colorScheme, children, buttons=null }) => {
    return (
        <Modal 
            onClose={onClose} 
            size={size} 
            isOpen={isOpen} 
            colorScheme={colorScheme}
            closeOnOverlayClick={false}>
            <ModalOverlay />
            <ModalContent>
                <ModalHeader style={{backgroundColor: "rgba(199, 202, 221, 0.2)", color: "#434343"}}>{title}</ModalHeader>
                <ModalCloseButton size="sm" style={{backgroundColor: "red", color: "white"}} />
                <ModalBody>
                    {children}
                </ModalBody>
                <ModalFooter>
                    {buttons}
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
};

export default ModalComponent;
