import React, { useState, useEffect } from 'react';
import axios from '../../axios';
import Loader from '../Loader/Loader';
import { showNotification } from '../ReactNotification/ReactNotification';
import { Form, Button } from 'react-bootstrap';
import { getErrorMessage } from '../../utils/helper';
import ErrorMessage from '../ErrorMessage/ErrorMessage';

const FacetCategoryType = ({ categoryId }) => {
    const [isSaving, setIsSaving] = useState(false);
    const [currentValue, setCurrentValue] = useState('');
    const [showError, setShowError] = useState(false);
    const [errorMsg, setErrorMsg] = useState(false);
    const [facetData, setFacetData] = useState({});

    const handleChange = (e) => {
        setCurrentValue(e.target.value);
    };

    const getFacetCategory = async (id) => {
        try {
            const { data } = await axios.get(`/classification/facet_category/${id}/`);
            console.log('data ', data);

            setCurrentValue(data?.facet_type);
            setFacetData({
                title: data?.title,
                description: data?.description,
            });
        } catch (error) {
            setShowError(true);
            setErrorMsg(getErrorMessage(error));
        }
    };

    useEffect(() => {
        if (categoryId) {
            getFacetCategory(categoryId);
        }
    }, [categoryId]);

    const saveFacetType = async (id) => {
        try {
            setIsSaving(true);
            const res = await axios.patch(`/classification/facet_category/${id}/`, {
                ...facetData,
                facet_type: currentValue,
            });
            if (res.status === 200) {
                setIsSaving(false);
                showNotification('Facet Category Type Successfully Updted');
            }
        } catch (error) {
            setIsSaving(false);
            setShowError(true);
            setErrorMsg(getErrorMessage(error));
        }
    };

    return (
        <div className="mb-5">
            <ErrorMessage show={showError} message={errorMsg} hide={() => setShowError(false)} />
            <h4 className="mb-3">Facet Category Type</h4>
            <Form.Group className="facet-value-row">
                <Form.Control as="select" onChange={handleChange} value={currentValue} custom>
                    <option value="" disabled>
                        Select
                    </option>
                    <option value="single">Single Select</option>
                    <option value="multi">Multi Select</option>
                    <option value="boolean">Boolean</option>
                </Form.Control>
            </Form.Group>
            <Button
                type="submit"
                className="centricity-btn"
                variant="primary"
                block
                onClick={() => saveFacetType(categoryId)}
            >
                {isSaving ? <Loader /> : 'Save'}
            </Button>
        </div>
    );
};

export default FacetCategoryType;
