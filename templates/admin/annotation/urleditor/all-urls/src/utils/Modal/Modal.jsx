import React from 'react';
import { Modal as BootstrapModal } from 'react-bootstrap';
import  SuccessIcon from '../../assets/svg/success-icon.svg';
import Button from '../Button/Button';
import './Modal.css';

const Modal = ({ show, onHide, className, backdrop, success, title, children }) => {
    return (
        <BootstrapModal
            show={show}
            onHide={onHide}
            className={success?.show ? 'success-modal' : className}
            backdrop={backdrop}
        >
            {success ? (
                <BootstrapModal.Body>
                    <div className="text-center p-5">
                        <SuccessIcon />
                        <p className="my-5" style={{ fontSize: '1.4rem' }}>
                            {success?.message}
                        </p>
                        <div>
                            <Button
                                title="Done"
                                className="custom-btn-primary rounded-border"
                                onClick={onHide}
                            />
                        </div>
                    </div>
                </BootstrapModal.Body>
            ) : (
                <>
                    <BootstrapModal.Header closeButton>
                        <BootstrapModal.Title>{title}</BootstrapModal.Title>
                    </BootstrapModal.Header>
                    <BootstrapModal.Body>{children}</BootstrapModal.Body>
                </>
            )}
        </BootstrapModal>
    );
};

export default Modal;
