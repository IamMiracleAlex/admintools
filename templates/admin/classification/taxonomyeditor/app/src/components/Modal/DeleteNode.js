import React, { useState } from 'react';
import axios from '../../axios';
import { Modal, Button } from 'react-bootstrap';
import { removeNodeAtPath, defaultGetNodeKey as getNodeKey } from 'react-sortable-tree';
import { showNotification } from '../ReactNotification/ReactNotification';
import ErrorMessage from '../ErrorMessage/ErrorMessage';
import { getErrorMessage } from '../../utils/helper';
import Loader from '../Loader/Loader';

const DeleteNode = ({ node, treeData, updateParentState }) => {
    const [isDeleting, setIsDeleting] = useState(false);
    const [showError, setShowError] = useState(false);
    const [errorMsg, setErrorMsg] = useState(false);

    const deleteNode = async (id) => {
        try {
            setIsDeleting(true);
            const res = await axios.delete(`classification/nodes/${id}/`);

            if (res.status === 204) {
                updateParentState({
                    showModal: false,
                    showDelete: false,
                    treeData: removeNodeAtPath({
                        treeData,
                        path: node.path,
                        getNodeKey,
                    }),
                    node: {},
                });
                setIsDeleting(false);
                showNotification('Node Successfully Deleted');
            }
        } catch (error) {
            setIsDeleting(false);
            setShowError(true);
            setErrorMsg(getErrorMessage(error));
        }
    };

    return (
        <>
            <Modal.Header closeButton>
                <Modal.Title>Delete Node</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <ErrorMessage
                    show={showError}
                    message={errorMsg}
                    hide={() => setShowError(false)}
                />
                <p>This node might have children. Are you sure you want to delete?</p>
            </Modal.Body>
            <Modal.Footer>
                <Button
                    className="centricity-btn"
                    variant="outline-primary"
                    onClick={() => updateParentState({ showModal: false, showDelete: false })}
                >
                    Cancel
                </Button>
                <Button
                    className=" centricity-btn"
                    variant="primary"
                    disabled={isDeleting}
                    onClick={() => deleteNode(node.node.id)}
                >
                    {isDeleting ? <Loader /> : 'Delete'}
                </Button>
            </Modal.Footer>
        </>
    );
};

export default DeleteNode;
