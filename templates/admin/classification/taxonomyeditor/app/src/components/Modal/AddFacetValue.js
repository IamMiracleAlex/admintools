import React, { useState, useEffect } from 'react';
import axios from '../../axios';
import { Modal, Form, Button } from 'react-bootstrap';
import Select from 'react-select';
import { showNotification } from '../ReactNotification/ReactNotification';
import ErrorMessage from '../ErrorMessage/ErrorMessage';
import { getErrorMessage } from '../../utils/helper';
import Loader from '../Loader/Loader';

const initialFormState = { label: '', description: '', category: null };

const AddFacetValue = ({ updateParentState }) => {
    const [formData, setFormData] = useState(initialFormState);
    const [isSaving, setIsSaving] = useState(false);
    const [showError, setShowError] = useState(false);
    const [errorMsg, setErrorMsg] = useState(false);
    const [facetCategoryOptions, setFacetCategoryOptions] = useState();

    useEffect(() => {
        const fetchFacetCategory = async () => {
            try {
                const res = await axios.get('/classification/facet_category/');
                if (res.status === 200) {
                    const options = res.data.map((facet) => ({
                        value: facet.id,
                        label: facet.title,
                    }));
                    setFacetCategoryOptions(options);
                }
            } catch (error) {
                setShowError(true);
            }
        };

        fetchFacetCategory();
    }, []);

    const handleInputChange = ({ target }) => {
        let { name, value } = target;
        value = name === 'label' ? value.toUpperCase() : value;
        setFormData({ ...formData, [name]: value });
    };

    const handleSelectChange = (value) => {
        setFormData({ ...formData, category: value });
    };

    const createFacetValue = async (data) => {
        try {
            setIsSaving(true);
            const res = await axios.post('classification/facet/', data);
            if (res.status === 201) {
                showNotification('Facet Value Successfully Created');
                updateParentState({
                    showModal: false,
                    showAddFacetValue: false,
                    refreshFacetValue: res.data,
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
        const { category, label, description } = formData;
        const data = {
            category: category?.value,
            label: label.replace(/ +(?= )/g, ''),
            description,
        };
        createFacetValue(data);
    };

    return (
        <>
            <Modal.Header closeButton>
                <Modal.Title>Facet Value</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <ErrorMessage
                    show={showError}
                    message={errorMsg}
                    hide={() => setShowError(false)}
                />

                <Form className="centricity-form pt-0" onSubmit={submitFacetCategory}>
                    <Form.Group>
                        <Form.Label>Category</Form.Label>
                        <Select
                            value={formData.category}
                            options={facetCategoryOptions}
                            onChange={handleSelectChange}
                            isLoading={!facetCategoryOptions}
                            className="custom-select-container"
                            classNamePrefix="custom-react-select"
                        />
                    </Form.Group>

                    <Form.Group className="mt-3">
                        <Form.Label>Label</Form.Label>
                        <Form.Control
                            type="text"
                            name="label"
                            value={formData.label}
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
                                updateParentState({ showModal: false, showAddFacetValue: false })
                            }
                        >
                            Cancel
                        </Button>
                        <Button
                            className=" centricity-btn"
                            variant="primary"
                            disabled={isSaving || !formData.category}
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

export default AddFacetValue;
