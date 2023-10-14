import React, { useState } from 'react';
import axios from '../axios';
import Button from '../utils/Button/Button';
import Modal from '../utils/Modal/Modal';
import Loader from '../utils/Loader/Loader';
import ErrorMessage from '../utils/ErrorMessage/ErrorMessage';
import { getErrorMessage } from '../utils/helper';

const ResetUrl = ({ selectedRows, assignSuccess }) => {
    const [show, setShow] = useState(false);
    const [isReseting, setIsReseting] = useState(false);
    const [showError, setShowError] = useState(false);
    const [errorMsg, setErrorMsg] = useState('');
    const [success, setSuccess] = useState(null);
    const numberOfUrls = selectedRows.length;

    const hideModal = () => {
        setShow(false);
        setShowError(false);
        setSuccess(null);
    };

    const resetUrl = async (data) => {
        try {
            setIsReseting(true);
            setShowError(false);

            const res = await axios.post('/annotation/urls/reset/', data);

            if (res.status === 205) {
                setIsReseting(false);
                setSuccess({
                    show: true,
                    message: `${numberOfUrls} URL(s) reset successful`,
                });
                assignSuccess();
            }
        } catch (error) {
            setErrorMsg(getErrorMessage(error));
            setIsReseting(false);
            setShowError(true);
        }
    };

    const onReset = () => {
        const urlIds = { url_ids: selectedRows.map((e) => e.id) };
        resetUrl(urlIds);
    };

    return (
        <>
            <Button
                title="Reset"
                className="custom-btn-primary w-110 mr-3"
                onClick={() => setShow(true)}
                disabled={numberOfUrls < 1}
            />
            {show && (
                <Modal
                    show={show}
                    onHide={hideModal}
                    title="Reset URL"
                    backdrop="static"
                    success={success}
                    className="delete-modal"
                >
                    <ErrorMessage
                        show={showError}
                        message={errorMsg}
                        hide={() => setShowError(false)}
                    />

                    <div className="bulk-assign-container">
                        <p style={{ fontSize: 18, paddingBottom: 16 }}>
                            Are you sure you want to reset the
                            <span className="font-weight-bold"> {numberOfUrls} </span>
                            selected URL(s)
                        </p>
                    </div>

                    <div className="float-right mt-4 mb-3">
                        <Button
                            title="Cancel"
                            className="custom-btn-primary-outline rounded-border mr-3"
                            disabled={isReseting}
                            onClick={hideModal}
                        />
                        <Button
                            type="submit"
                            title={isReseting ? <Loader /> : 'Yes, Proceed'}
                            disabled={isReseting}
                            className="custom-btn-primary rounded-border"
                            onClick={onReset}
                        />
                    </div>
                </Modal>
            )}
        </>
    );
};

export default ResetUrl;
