import React, { useState } from 'react';
import axios from '../../axios';
import { Modal, Form, Button } from 'react-bootstrap';
import { showNotification } from '../ReactNotification/ReactNotification';
import ErrorMessage from '../ErrorMessage/ErrorMessage';
import { getErrorMessage } from '../../utils/helper';
import Loader from '../Loader/Loader';

const initialFormState = { title: '', description: '', facets: [] };

const AddFacetCategory = ({ showAddFacetCategory, updateParentState }) => {
    const [formData, setFormData] = useState(initialFormState);
    const [isSaving, setIsSaving] = useState(false);
    const [showError, setShowError] = useState(false);
    const [errorMsg, setErrorMsg] = useState(false);

    const handleInputChange = ({ target }) => {
        let { name, value } = target;
        value =
            name === 'title'
                ? value.replace(/ +(?= )/g, '').toUpperCase()
                : value.replace(/ +(?= )/g, '');
        setFormData({ ...formData, [name]: value });
    };

    const createFacetCategory = async () => {
        try {
            setIsSaving(true);
            const res = await axios.post('classification/facet_category/', formData);
            if (res.status === 201) {
                showNotification('Facet Successfully Created');
                updateParentState({
                    showModal: false,
                    showAddFacetCategory: false,
                    refreshFacetCategory: res.data,
                });
            }
        } catch (error) {
            setIsSaving(false);
            setShowError(true);
            setErrorMsg(getErrorMessage(error));
        }
    };

    const submitFacetCategory = (e) => {
        e.preventDefault();
        createFacetCategory();
    };

    return (
        <>
            <Modal.Header closeButton>
                <Modal.Title>Facet Category</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <ErrorMessage
                    show={showError}
                    message={errorMsg}
                    hide={() => setShowError(false)}
                />
                <Form onSubmit={submitFacetCategory} className="centricity-form pt-0">
                    <Form.Group>
                        <Form.Label>Title</Form.Label>
                        <Form.Control
                            type="text"
                            name="title"
                            value={formData.title}
                            onChange={handleInputChange}
                            required
                        />
                    </Form.Group>
                    <Form.Group className="mt-3">
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows="3"
                            name="description"
                            value={formData.description}
                            onChange={handleInputChange}
                        />
                    </Form.Group>
                    <div className="add-facet-modal-footer">
                        <Button
                            className="centricity-btn mr-2"
                            variant="outline-primary"
                            onClick={() =>
                                updateParentState({
                                    showModal: false,
                                    showAddFacetCategory: false,
                                })
                            }
                        >
                            Cancel
                        </Button>
                        <Button
                            className=" centricity-btn"
                            variant="primary"
                            disabled={isSaving}
                            type="submit"
                        >
                            {isSaving ? <Loader /> : 'Save'}
                        </Button>
                    </div>
                </Form>
            </Modal.Body>
        </>
    );
};

export default AddFacetCategory;
