import React, { useState } from 'react';
import axios from '../axios';
import Button from '../utils/Button/Button';
import Modal from '../utils/Modal/Modal';
import Loader from '../utils/Loader/Loader';
import ErrorMessage from '../utils/ErrorMessage/ErrorMessage';
import { getErrorMessage } from '../utils/helper';

const DeleteUrl = ({ selectedRows, assignSuccess }) => {
    const [show, setShow] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [showError, setShowError] = useState(false);
    const [errorMsg, setErrorMsg] = useState('');
    const [success, setSuccess] = useState(null);
    const numberOfUrls = selectedRows.length;

    const hideModal = () => {
        setShow(false);
        setShowError(false);
        setSuccess(null);
    };

    const deleteUrl = async (data) => {
        try {
            setIsDeleting(true);
            setShowError(false);

            const res = await axios.delete('/annotation/urls/delete/', { data });

            if (res.status === 204) {
                setIsDeleting(false);
                setSuccess({
                    show: true,
                    message: `You have successfully deleted ${numberOfUrls} URL(s)`,
                });
                assignSuccess();
            }
        } catch (error) {
            setErrorMsg(getErrorMessage(error));
            setIsDeleting(false);
            setShowError(true);
        }
    };

    const onDelete = () => {
        const urlIds = { url_ids: selectedRows.map((e) => e.id) };
        deleteUrl(urlIds);
    };

    return (
        <>
            <Button
                title="Delete"
                className="custom-btn-primary w-110 mr-3"
                onClick={() => setShow(true)}
                disabled={numberOfUrls < 1}
            />
            {show && (
                <Modal
                    show={show}
                    onHide={hideModal}
                    title="Delete URL"
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
                            Are you sure you want to delete the
                            <span className="font-weight-bold"> {numberOfUrls} </span>
                            selected URL(s)
                        </p>
                    </div>

                    <div className="float-right mt-4 mb-3">
                        <Button
                            title="Cancel"
                            className="custom-btn-primary-outline rounded-border mr-3"
                            disabled={isDeleting}
                            onClick={hideModal}
                        />
                        <Button
                            type="submit"
                            title={isDeleting ? <Loader /> : 'Yes, Proceed'}
                            disabled={isDeleting}
                            className="custom-btn-primary rounded-border"
                            onClick={onDelete}
                        />
                    </div>
                </Modal>
            )}
        </>
    );
};

export default DeleteUrl;
