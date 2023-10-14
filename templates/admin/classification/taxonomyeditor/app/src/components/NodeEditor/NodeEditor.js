import React, { useState, useEffect } from 'react';
import axios from '../../axios';
import { Row, Col, Form, Button } from 'react-bootstrap';
import { changeNodeAtPath, defaultGetNodeKey as getNodeKey } from 'react-sortable-tree';
import { showNotification } from '../ReactNotification/ReactNotification';
import { getErrorMessage, canEdit } from '../../utils/helper';
import ErrorMessage from '../ErrorMessage/ErrorMessage';
import Loader from '../Loader/Loader';
import FacetCategoryType from './FacetCategoryType';
import { ReactComponent as SearchIcon } from '../../assets/svg/search-icon.svg';

const initialFormData = { title: '', description: '', facet_properties: [] };

const NodeEditor = ({
    onClickNode,
    treeData,
    updateParentState,
    refreshFacetCategory,
    refreshFacetValue,
    fetchingFacets,
}) => {
    const [facetsCategory, setFacetsCategory] = useState([]);
    const [facetsCateFiltered, setFacetsCateFiltered] = useState([]);
    const [facetValue, setFacetValue] = useState([]);
    const [facetValueFiltered, setFacetValueFiltered] = useState([]);
    const [facetCategoryId, setFacetCategoryId] = useState(null);
    const [isSaving, setIsSaving] = useState(false);
    const [isFetchingFacets, setIsFetchingFacets] = useState(false);
    const [showError, setShowError] = useState(false);
    const [errorMsg, setErrorMsg] = useState(false);
    const [formData, setFormData] = useState(initialFormData);
    const [updatedFacetValues, setUpdatedFacetValues] = useState([]);
    const [facetCategoryTypeFilter, setFacetCategoryTypeFilter] = useState('all');
    const { title, description, facet_properties } = formData;

    const fetchFacetCategory = async () => {
        try {
            const { data } = await axios.get('/classification/facet_category/');
            setFacetsCategory(data);
            setFacetsCateFiltered(data);
        } catch (error) {
            setShowError(true);
            setErrorMsg(getErrorMessage(error));
        }
    };

    const fetchFacetsValue = async () => {
        try {
            const { data } = await axios.get('/classification/facet/');
            setFacetValue(data);
            setFacetValueFiltered(data);
        } catch (error) {
            setShowError(true);
            setErrorMsg(getErrorMessage(error));
        }
    };

    useEffect(() => {
        fetchFacetCategory();
        fetchFacetsValue();
    }, [refreshFacetCategory, refreshFacetValue]);

    useEffect(() => {
        if (onClickNode) {
            const { parentNode, node } = onClickNode;
            let newFormDataOnClickNode = {
                title: node.title,
                description: node.description,
                facet_properties: node.facet_properties?.map((facet) => ({
                    has_facet: facet.has_facet,
                    facet: facet.id,
                })),
                parent: parentNode ? parentNode.id : null,
            };
            setFormData(newFormDataOnClickNode);
            setFacetCategoryId(null);
        }
    }, [onClickNode]);

    useEffect(() => setIsFetchingFacets(fetchingFacets), [fetchingFacets]);

    const setStateOnSave = (nodeData) => {
        setIsSaving(false);
        const newFacetObject = facet_properties?.map(({ facet, has_facet }) => ({
            id: facet,
            has_facet,
        }));
        updateParentState({
            treeData: changeNodeAtPath({
                treeData,
                path: onClickNode.path,
                getNodeKey,
                newNode: { ...onClickNode.node, ...nodeData, facet_properties: newFacetObject },
            }),
            nodeClicked: null,
        });
        setFormData(initialFormData);
        setUpdatedFacetValues([]);
        setFacetCategoryId(null);
    };

    const createNewNode = async () => {
        try {
            setIsSaving(true);
            const res = await axios.post('classification/nodes/', {
                title: title.replace(/ +(?= )/g, ''),
                description,
                facet_properties: updatedFacetValues,
                ...(formData.hasOwnProperty('parent') && { parent: formData.parent }),
            });
            if (res.status === 201) {
                showNotification('Node Successfully Created');
                setStateOnSave(res.data);
            }
        } catch (error) {
            setIsSaving(false);
            setShowError(true);
            setErrorMsg(getErrorMessage(error));
        }
    };

    const updateCurrentNode = async () => {
        const { node } = onClickNode;
        try {
            setIsSaving(true);
            const res = await axios.patch(`classification/nodes/${node.id}/`, {
                title: title.replace(/ +(?= )/g, ''),
                description,
                facet_properties: updatedFacetValues,
            });
            if (res.status === 200) {
                showNotification('Node Successfully Updated');
                setStateOnSave(res.data);
            }
        } catch (error) {
            setIsSaving(false);
            setShowError(true);
            setErrorMsg(getErrorMessage(error));
        }
    };

    const disableSaveBtn = title === '' && description === '' && facet_properties < 1;

    const handleInputChange = ({ target }) => {
        let { name, value } = target;
        value = name === 'title' ? value.toUpperCase() : value;
        setFormData({ ...formData, [name]: value });
    };

    const handleSelectChange = (e, id) => {
        const facetIndex = facet_properties.findIndex(({ facet }) => facet === id);
        const updatedFacetIndex = updatedFacetValues.findIndex(({ facet }) => facet === id);
        // If facet does not exist in the array, create a new one
        if (facetIndex < 0) {
            setFormData({
                ...formData,
                facet_properties: [
                    ...facet_properties,
                    {
                        facet: id,
                        has_facet: e.target.value,
                    },
                ],
            });
        } else {
            // Edit existing facet
            let facetsArray = [...facet_properties];
            facetsArray[facetIndex] = { ...facetsArray[facetIndex], has_facet: e.target.value };
            setFormData({
                ...formData,
                facet_properties: [...facetsArray],
            });
            // setUpdatedFacetValues([...facetsArray]);
        }

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
        const filteredCategory = facetValueFiltered.filter(
            (item) => item.category === facetCategoryId,
        );

        const newFacet = filteredCategory.map((item) => ({
            facet: item.id,
            has_facet: e.target.value,
        }));

        const newFacetProperties = formData.facet_properties.map((item) => ({
            facet: item.facet,
            has_facet: filteredCategory.find((cate) => cate.id === item.facet)
                ? e.target.value
                : item.has_facet,
        }));

        setUpdatedFacetValues(newFacet);
        setFormData({
            ...formData,
            facet_properties: newFacetProperties,
        });
    };

    const renderFacetValue = () => {
        return facetValueFiltered
            .filter(({ category }) => category === facetCategoryId)
            ?.map(({ id, label }) => (
                <Form.Group key={id} className="facet-value-row">
                    <Form.Label>{label}</Form.Label>
                    <Form.Control
                        as="select"
                        className="facet-value-select"
                        onChange={(e) => handleSelectChange(e, id)}
                        value={facet_properties?.find(({ facet }) => facet === id)?.has_facet || ''}
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
            ));
    };

    const onSubmitNode = (e) => {
        e.preventDefault();
        // if node has id update node else create new node
        onClickNode.node.id ? updateCurrentNode() : createNewNode();
    };

    const handleFacetTypeFilterChange = (e) => {
        setFacetCategoryTypeFilter(e.target.value);
        if (e.target.value === 'all') {
            return setFacetsCateFiltered(facetsCategory);
        }
        setFacetsCateFiltered(facetsCategory.filter((ya) => ya.facet_type === e.target.value));
    };

    const handleSearchOnChange = (e) => {
        const value = e.target.value;
        setFacetsCateFiltered(
            facetsCategory.filter(
                (i) => i.title.toLowerCase().indexOf(value.toLowerCase().trim()) !== -1,
            ),
        );
    };

    const handleFacetValueSearchOnChange = (e) => {
        const value = e.target.value;
        setFacetValueFiltered(
            facetValue.filter(
                (i) => i.label.toLowerCase().indexOf(value.toLowerCase().trim()) !== -1,
            ),
        );
    };

    return (
        <Row>
            <Col lg={6} md={12}>
                <div className="column-container node-editor">
                    <ErrorMessage
                        show={showError}
                        message={errorMsg}
                        hide={() => setShowError(false)}
                    />
                    <h4>Node Editor</h4>

                    <Form onSubmit={onSubmitNode} className="centricity-form">
                        <Form.Group>
                            <Form.Label>Title:</Form.Label>
                            <Form.Control
                                type="text"
                                name="title"
                                value={title}
                                disabled={!onClickNode}
                                onChange={handleInputChange}
                                required
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Description:</Form.Label>
                            <Form.Control
                                as="textarea"
                                rows="3"
                                name="description"
                                value={description}
                                disabled={!onClickNode}
                                onChange={handleInputChange}
                            />
                        </Form.Group>
                        <h4 className="pt-2">The Facet Category</h4>
                        {/* Facet category filteer */}
                        <div className="mt-3">
                            <p style={{ fontSize: 14 }}>Category Type</p>
                            <div className="d-flex">
                                <Form.Group className="facet-category-filter">
                                    <Form.Control
                                        as="select"
                                        onChange={handleFacetTypeFilterChange}
                                        value={facetCategoryTypeFilter}
                                        custom
                                    >
                                        <option value="" disabled>
                                            Select
                                        </option>
                                        <option value="all">All</option>
                                        <option value="single">Single Select</option>
                                        <option value="multi">Multi Select</option>
                                        <option value="boolean">Boolean</option>
                                    </Form.Control>
                                </Form.Group>
                                <div className="node-editor-search">
                                    <Form.Control
                                        className="custom-search"
                                        placeholder="Search"
                                        onChange={handleSearchOnChange}
                                    />
                                    <SearchIcon />
                                </div>
                            </div>
                        </div>

                        <div className="facet-btn-container facet-category">
                            {isFetchingFacets ? (
                                <Loader size="lg" />
                            ) : facetsCateFiltered && facetsCateFiltered.length > 0 ? (
                                facetsCateFiltered?.map(({ id, title }) => {
                                    const highlighted = id === facetCategoryId ? 'highlighted' : '';
                                    return (
                                        <Button
                                            key={id}
                                            className={`facet-btn ${highlighted}`}
                                            variant="outline-primary"
                                            onClick={() => {
                                                setFacetCategoryId(id);
                                                setFacetValueFiltered(facetValue);
                                            }}
                                            disabled={!onClickNode}
                                            block
                                        >
                                            {title}
                                        </Button>
                                    );
                                })
                            ) : (
                                'No facet category found'
                            )}
                        </div>
                        <Button
                            type="submit"
                            className="centricity-btn"
                            variant="primary"
                            disabled={isSaving}
                            block
                        >
                            {isSaving ? <Loader /> : 'Save'}
                        </Button>
                    </Form>
                </div>
            </Col>

            {/* Facet Value Column */}
            {facetCategoryId && (
                <Col lg={6} md={12}>
                    <div className="column-container node-editor facet-value-wrapper">
                        <FacetCategoryType categoryId={facetCategoryId} />
                        <h4>Facet Value</h4>
                        <div className="mt-3">
                            <div className="node-editor-search ml-0 w-100 ">
                                <Form.Control
                                    className="custom-search"
                                    placeholder="Search"
                                    onChange={handleFacetValueSearchOnChange}
                                />
                                <SearchIcon />
                            </div>
                        </div>
                        <div className="mt-3">
                            <div className="node-editor-search ml-0 w-100 ">
                                <p style={{ fontSize: 14 }}>Edit All</p>
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
                        <div className="facet-btn-container">{renderFacetValue()}</div>
                    </div>
                </Col>
            )}
        </Row>
    );
};

export default NodeEditor;
