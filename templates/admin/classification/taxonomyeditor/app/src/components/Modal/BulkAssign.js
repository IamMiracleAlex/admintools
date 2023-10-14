import React, { useState, useEffect } from 'react';
import axios from '../../axios';
import { Modal, Button, Row, Col, Form } from 'react-bootstrap';
import { getErrorMessage } from '../../utils/helper';
import ErrorMessage from '../ErrorMessage/ErrorMessage';
import { showNotification } from '../ReactNotification/ReactNotification';
import Loader from '../Loader/Loader';

const BulkAssign = ({ selectedNodes, updateState }) => {
    const [show, setShow] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [isFetchingFacets, setIsFetchingFacets] = useState(false);
    const [showError, setShowError] = useState(false);
    const [errorMsg, setErrorMsg] = useState(false);
    const [facetCategoryId, setFacetCategoryId] = useState(null);
    const [facetsCategory, setFacetsCategory] = useState([]);
    const [facetValue, setFacetValue] = useState([]);
    const [updatedFacetValues, setUpdatedFacetValues] = useState([]);
    const [nodesSelected, setNodesSelected] = useState(selectedNodes.map((e) => e.id));

    const hideModal = () => {
        setShow(false);
        setShowError(false);
        setUpdatedFacetValues([]);
        setNodesSelected([]);
        setFacetValue([]);
        setFacetCategoryId(null);
        updateState({ selectedNodes: [], selectAll: false });
    };

    useEffect(() => {
        if (show) {
            const fetchFacetCategory = async () => {
                try {
                    setIsFetchingFacets(true);
                    const { data } = await axios.get('/classification/facet_category/');
                    setFacetsCategory(data);
                    setIsFetchingFacets(false);
                } catch (error) {
                    setShowError(true);
                    setErrorMsg(getErrorMessage(error));
                    setIsFetchingFacets(false);
                }
            };

            const fetchFacetsValue = async () => {
                try {
                    const { data } = await axios.get('/classification/facet/');
                    setFacetValue(data);
                } catch (error) {
                    setShowError(true);
                    setErrorMsg(getErrorMessage(error));
                }
            };

            fetchFacetCategory();
            fetchFacetsValue();
        }
    }, [show]);

    useEffect(() => {
        setNodesSelected(selectedNodes.map((e) => e.id));
    }, [selectedNodes]);

    const handleSelectChange = (e, id) => {
        const updatedFacetIndex = updatedFacetValues.findIndex(({ facet }) => facet === id);
        // If facet does not exist in the array, create a new one
        if (updatedFacetIndex < 0) {
            setUpdatedFacetValues([
                ...updatedFacetValues,
                {
                    facet: id,
                    has_facet: e.target.value,
                },
            ]);
        } else {
            let facetsArray = [...updatedFacetValues];
            facetsArray[updatedFacetIndex] = {
                ...facetsArray[updatedFacetIndex],
                has_facet: e.target.value,
            };
            setUpdatedFacetValues([...facetsArray]);
        }
    };

    const handleControlledSelect = (e) => {
        const filteredCategory = facetValue.filter((item) => item.category === facetCategoryId);

        const newFacet = filteredCategory.map((item) => ({
            facet: item.id,
            has_facet: e.target.value,
        }));

        setUpdatedFacetValues(newFacet);
    };

    const postBulkAssign = async () => {
        try {
            setIsSaving(true);
            const res = await axios.post('classification/nodes/bulk_assign_facets/', {
                nodes: nodesSelected,
                facets: updatedFacetValues,
            });
            if (res.status === 200) {
                showNotification(`${selectedNodes.length} nodes successfully assigned`);
                setShow(false);
                setIsSaving(false);
                setUpdatedFacetValues([]);
                setNodesSelected([]);
                hideModal();
            }
        } catch (error) {
            setIsSaving(false);
            setShowError(true);
            setErrorMsg(getErrorMessage(error));
        }
    };

    return (
        <>
            <Button
                className="custom-btn-primary mr-2"
                variant="primary"
                onClick={() => setShow(true)}
                disabled={selectedNodes < 1}
            >
                Bulk Assign
            </Button>

            {show && (
                <Modal
                    show={show}
                    onHide={hideModal}
                    className="bulk-assign-modal"
                    backdrop="static"
                >
                    <Modal.Header closeButton>
                        <Modal.Title>Bulk Assign</Modal.Title>
                    </Modal.Header>
                    <div className="px-3">
                        <ErrorMessage
                            show={showError}
                            message={errorMsg}
                            hide={() => setShowError(false)}
                        />
                        <h4 className="pt-3 font-bold">{nodesSelected.length} nodes selected</h4>
                        <Row>
                            <Col lg={6} md={6}>
                                <div className="facet-btn-container facet-category bulk-assign-facet">
                                    {isFetchingFacets ? (
                                        <Loader size="lg" />
                                    ) : (
                                        <>
                                            <h4 className="pb-3">The Facet Category</h4>
                                            {facetsCategory.map(({ id, title }) => {
                                                const highlighted =
                                                    id === facetCategoryId ? 'highlighted' : '';
                                                return (
                                                    <Button
                                                        key={id}
                                                        className={`facet-btn ${highlighted}`}
                                                        variant="outline-primary"
                                                        onClick={() => setFacetCategoryId(id)}
                                                        block
                                                    >
                                                        {title}
                                                    </Button>
                                                );
                                            })}
                                        </>
                                    )}
                                </div>
                            </Col>
                            <Col lg={6} md={6}>
                                {facetCategoryId && (
                                    <div className="facet-btn-container facet-category bulk-assign-facet">
                                        <div className="mt-3">
                                            <div className="node-editor-search ml-0 w-100 ">
                                                <p style={{ fontSize: 16 }}>Edit All</p>
                                                <Form.Group className="facet-value-row">
                                                    <Form.Control
                                                        as="select"
                                                        onChange={handleControlledSelect}
                                                        custom
                                                    >
                                                        <option value="">Select</option>
                                                        <option value="always">Always</option>
                                                        <option value="sometimes">Sometimes</option>
                                                        <option value="never">Never</option>
                                                    </Form.Control>
                                                </Form.Group>
                                            </div>
                                        </div>
                                        {facetValue
                                            .filter(({ category }) => category === facetCategoryId)
                                            .map(({ id, label }) => (
                                                <Form.Group key={id} className="facet-value-row">
                                                    <Form.Label>{label}</Form.Label>
                                                    <Form.Control
                                                        as="select"
                                                        className="facet-value-select"
                                                        onChange={(e) => handleSelectChange(e, id)}
                                                        value={
                                                            updatedFacetValues?.find(
                                                                ({ facet }) => facet === id,
                                                            )?.has_facet || ''
                                                        }
                                                        custom
                                                    >
                                                        <option value="" disabled>
                                                            Select
                                                        </option>
                                                        <option value="always">Always</option>
                                                        <option value="sometimes">Sometimes</option>
                                                        <option value="never">Never</option>
                                                    </Form.Control>
                                                </Form.Group>
                                            ))}
                                    </div>
                                )}
                            </Col>
                        </Row>
                        <div className="add-facet-modal-footer pb-4">
                            <Button
                                className="centricity-btn mr-2"
                                variant="outline-primary"
                                onClick={hideModal}
                                disabled={isSaving}
                            >
                                Cancel
                            </Button>
                            <Button
                                className=" centricity-btn"
                                variant="primary"
                                disabled={isSaving}
                                type="button"
                                onClick={postBulkAssign}
                            >
                                {isSaving ? <Loader /> : 'Save'}
                            </Button>
                        </div>
                    </div>
                </Modal>
            )}
        </>
    );
};

export default BulkAssign;
