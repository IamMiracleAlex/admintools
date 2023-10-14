import React, { useEffect, useState } from 'react';
import axios from '../../axios';
import { Modal, Button, Form, Alert } from 'react-bootstrap';
import { showNotification } from '../ReactNotification/ReactNotification';
import { getErrorMessage, exportCSVFile } from '../../utils/helper';

import ErrorMessage from '../ErrorMessage/ErrorMessage';
import ReactSelect from 'react-select';
import Loader from '../Loader/Loader';
import { format } from 'date-fns';

const ExportHierarchy = ({ treeData, updateParentState, selectedNodes }) => {
    const [exportFormat, setExportFormat] = useState('');
    const [selectedRadioBtn, setSelectedRadioBtn] = useState('hierarchyExport');
    const [departmentData, setDepartmentData] = useState();
    const [facetsData, setFacetsData] = useState([]);
    const [facetTyoe, setFacetTyoe] = useState([]);
    const [selectedDept, setSelectedDept] = useState('');
    const [isExporting, setIsExporting] = useState(false);
    const [isSendingVerificationEmail, setIsSendingVerificationEmail] = useState(false);
    const [showError, setShowError] = useState(false);
    const [errorMsg, setErrorMsg] = useState(false);
    const [alertText, setAlertText] = useState('');
    const [hasVerifiedEmail, setHasVerifiedEmail] = useState(true);

    useEffect(() => {
        fetchDepartments();
        getAllFacets();
    }, []);

    const fetchDepartments = async () => {
        try {
            const { data } = await axios.get('/classification/nodes/?level=0');

            setDepartmentData(
                data.map((dept) => ({
                    value: dept.id,
                    label: dept.title,
                })),
            );
        } catch (error) {}
    };

    const getAllFacets = async () => {
        try {
            const res = await axios.get('/classification/facet_category/');
            if (res.status === 200) {
                const facetsArray = [];
                res?.data.forEach((category) => {
                    category.facets.forEach((facet) => {
                        let facetObject = {
                            facetCategory: category.title,
                            facetValue: facet.label,
                            dateCreated: format(Date.parse(facet.created_at), 'MMM-dd-yyyy'),
                        };
                        facetsArray.push(facetObject);
                    });
                });
                setFacetsData(facetsArray);
                setFacetTyoe(
                    res.data.map((data) => ({
                        facetCategory: data.title,
                        facetType: data.facet_type,
                    })),
                );
            }
        } catch (error) {}
    };

    const handleSelectChange = (e) => setExportFormat(e.target.value);

    const handleReactSelectChange = (e) => {
        setSelectedDept(e.value);
    };

    const handleRadioBtnChange = (e) => {
        setSelectedRadioBtn(e.target.value);
        if (e.target.value === 'hierarchyExport') {
            setSelectedDept('');
            setAlertText('');
        } else {
            setExportFormat('');
        }
    };

    const exportHierarchyToCSV = () => {
        const csvData = [];
        treeData.forEach((level1) => {
            csvData.push({
                department: `"${level1.title}"`,
                category: '',
                subCategory: '',
                subset: '',
                created_at: `"${format(Date.parse(level1.created_at), 'MMM-dd-yyyy')}"`,
            });
            level1.children &&
                level1.children.forEach((level2) => {
                    csvData.push({
                        department: `"${level1.title}"`,
                        category: `"${level2.title}"`,
                        subCategory: '',
                        subset: '',
                        created_at: `"${format(Date.parse(level2.created_at), 'MMM-dd-yyyy')}"`,
                    });
                    level2.children &&
                        level2.children.forEach((level3) => {
                            csvData.push({
                                department: `"${level1.title}"`,
                                category: `"${level2.title}"`,
                                subCategory: `"${level3.title}"`,
                                subset: '',
                                created_at: `"${format(Date.parse(level3.created_at), 'MMM-dd-yyyy')}"`,
                            });
                            level3.children &&
                                level3.children.forEach((level4) => {
                                    csvData.push({
                                        department: `"${level1.title}"`,
                                        category: `"${level2.title}"`,
                                        subCategory: `"${level3.title}"`,
                                        subset: `"${level4.title}"`,
                                        created_at: `"${format(Date.parse(level4.created_at), 'MMM-dd-yyyy')}"`,
                                    });
                                });
                        });
                });
        });

        const headers = {
            department: 'DEPARTMENT',
            category: 'CATEGORY',
            subCategory: 'SUBCATEGORY',
            subset: 'SUBSET',
            created_at: 'DATE CREATED (for leaf nodes)',
        };

        exportCSVFile(headers, csvData, 'hierarchyExport');
    };

    const exportDataToJSON = () => {
        const jsonContent =
            'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(treeData));
        const link = document.createElement('a');
        link.setAttribute('href', jsonContent);
        link.setAttribute('download', 'hierarchyData.json');
        document.body.appendChild(link);

        link.click();
    };

    const exportFacetToCSV = () => {
        const headers = {
            facetCategory: 'Facet Category',
            facetValue: 'Facet Value',
            dateCreated: 'Date Created',
        };
        exportCSVFile(headers, facetsData, 'facetExports');
    };

    const exportFacetType = () => {
        const headers = {
            facetCategory: 'Facet Category',
            facetType: 'Facet Type',
        };
        exportCSVFile(headers, facetTyoe, 'facetType');
    };

    const exportFacet = async () => {
        try {
            setIsExporting(true);
            const res = await axios.get(
                `/classification/nodes/${selectedDept}/download_facet_extract/`,
            );

            if (res.status === 200) {
                setIsExporting(false);
                const downloadUrl = window.URL.createObjectURL(new Blob([res.data]));
                const link = document.createElement('a');
                link.href = downloadUrl;
                const departmentName = departmentData.find((e) => e.value === selectedDept)?.label;
                link.setAttribute('download', `${departmentName}_facets.csv`);
                document.body.appendChild(link);
                link.click();
                link.remove();
                showNotification('Facet extract successful');
                updateParentState({ showModal: false, showExport: false });
            }

            if (res.status === 202) {
                if (sessionStorage.getItem('email_verified') === 'True') {
                    showNotification('Facet extract will be sent to your email');
                    updateParentState({ showModal: false, showExport: false });
                } else {
                    setIsExporting(false);
                    setAlertText(res.data?.detail);
                    setHasVerifiedEmail(false);
                }
            }
            setIsExporting(false);
        } catch (error) {
            setIsExporting(false);
            setShowError(true);
            setErrorMsg(getErrorMessage(error));
        }
    };

    const exportNodeAndFacet = async () => {
        try {
            setIsExporting(true);
            const res = await axios.get(
                `/classification/nodes/${selectedNodes[0].id}/download_facet_category_extract/`,
            );

            if (res.status === 200) {
                setIsExporting(false);
                const downloadUrl = window.URL.createObjectURL(new Blob([res.data]));
                const link = document.createElement('a');
                link.href = downloadUrl;
                link.setAttribute('download', `exportWithFacetCategory.csv`);
                document.body.appendChild(link);
                link.click();
                link.remove();
                showNotification('Facet exported successfully');
                updateParentState({ showModal: false, showExport: false, selectedNodes: [] });
            }

            if (res.status === 202) {
                if (sessionStorage.getItem('email_verified') === 'True') {
                    showNotification('Facet extract will be sent to your email');
                    updateParentState({ showModal: false, showExport: false });
                } else {
                    setIsExporting(false);
                    setAlertText(res.data?.detail);
                    setHasVerifiedEmail(false);
                }
            }
            setIsExporting(false);
        } catch (error) {
            setIsExporting(false);
            setShowError(true);
            setErrorMsg(getErrorMessage(error));
        }
    };

    const verifyEmail = async () => {
        try {
            setIsSendingVerificationEmail(true);
            const res = await axios.get('/server/verify-email');

            if (res.status === 200) {
                setIsSendingVerificationEmail(false);
                showNotification('Verification Email Successfully Sent');
                updateParentState({ showModal: false, showExport: false });
            }
        } catch (error) {
            setIsSendingVerificationEmail(false);
            setShowError(true);
            setErrorMsg(getErrorMessage(error));
        }
    };

    const exportData = () => {
        if (selectedRadioBtn === 'hierarchyExport') {
            if (exportFormat === '.csv') {
                exportHierarchyToCSV();
            } else if (exportFormat === '.json') {
                exportDataToJSON();
            }
            updateParentState({ showModal: false, showExport: false });
        } else if (selectedRadioBtn === 'nodeWithFacet') {
            exportFacet();
        } else if (selectedRadioBtn === 'allFacets') {
            exportFacetToCSV();
        } else if (selectedRadioBtn === 'facetType') {
            exportFacetType();
            updateParentState({ showModal: false, showExport: false });
        } else if (selectedRadioBtn === 'nodeAndFacet') {
            if (selectedNodes.length < 1) {
                setShowError(true);
                const error = {
                    message: 'Please select a node'
                }
                setErrorMsg(getErrorMessage(error));
            } else {
                exportNodeAndFacet();
            }
        }
    };

    return (
        <>
            <Modal.Header closeButton>
                <Modal.Title>Export Hierarchy</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <div className="my-3">
                    <ErrorMessage
                        show={showError}
                        message={errorMsg}
                        hide={() => setShowError(false)}
                    />
                </div>
                <div className="pb-4">
                    <div className="form-check form-check-inline mr-4">
                        <label className="form-check-label">
                            <input
                                className="form-check-input"
                                type="radio"
                                value="hierarchyExport"
                                checked={selectedRadioBtn === 'hierarchyExport'}
                                onChange={handleRadioBtnChange}
                            />
                            Export Hierarchy
                        </label>
                    </div>
                    <div className="form-check form-check-inline">
                        <label className="form-check-label">
                            <input
                                className="form-check-input"
                                type="radio"
                                value="nodeWithFacet"
                                checked={selectedRadioBtn === 'nodeWithFacet'}
                                onChange={handleRadioBtnChange}
                            />
                            Export node with facets
                        </label>
                    </div>
                    <div className="form-check form-check-inline">
                        <label className="form-check-label">
                            <input
                                className="form-check-input"
                                type="radio"
                                value="allFacets"
                                checked={selectedRadioBtn === 'allFacets'}
                                onChange={handleRadioBtnChange}
                            />
                            Export all facet categories
                        </label>
                    </div>
                    <div className="form-check form-check-inline">
                        <label className="form-check-label">
                            <input
                                className="form-check-input"
                                type="radio"
                                value="facetType"
                                checked={selectedRadioBtn === 'facetType'}
                                onChange={handleRadioBtnChange}
                            />
                            Export facet type
                        </label>
                    </div>
                    <div className="form-check form-check-inline">
                        <label className="form-check-label">
                            <input
                                className="form-check-input"
                                type="radio"
                                value="nodeAndFacet"
                                checked={selectedRadioBtn === 'nodeAndFacet'}
                                onChange={handleRadioBtnChange}
                            />
                            Export node and facet information
                        </label>
                    </div>
                </div>

                {selectedRadioBtn === 'hierarchyExport' && (
                    <Form.Group>
                        <Form.Control as="select" size="md" onChange={handleSelectChange}>
                            <option value="">Format</option>
                            <option value=".csv">CSV</option>
                            <option value=".json">JSON</option>
                        </Form.Control>
                    </Form.Group>
                )}

                {selectedRadioBtn === 'nodeWithFacet' && (
                    <>
                        {!hasVerifiedEmail && (
                            <Alert variant="primary" className="text-center py-4">
                                <div>
                                    {alertText}
                                    <br />
                                    <br />
                                    You need to <b>verify your email</b> to receive messages. Click
                                    on the button below &#128071; to verify
                                    <div className="mt-4">
                                        <Button
                                            className=" centricity-btn m-auto"
                                            variant="primary"
                                            onClick={verifyEmail}
                                        >
                                            {isSendingVerificationEmail ? (
                                                <Loader />
                                            ) : (
                                                'Send Verification Email'
                                            )}
                                        </Button>
                                    </div>
                                </div>
                            </Alert>
                        )}
                        <ReactSelect
                            onChange={handleReactSelectChange}
                            options={departmentData}
                            isLoading={!departmentData}
                        />
                    </>
                )}
                {selectedRadioBtn === 'nodeAndFacet' && (
                    <>
                        {!hasVerifiedEmail && (
                            <Alert variant="primary" className="text-center py-4">
                                <div>
                                    {alertText}
                                    <br />
                                    <br />
                                    You need to <b>verify your email</b> to receive messages. Click
                                    on the button below &#128071; to verify
                                    <div className="mt-4">
                                        <Button
                                            className=" centricity-btn m-auto"
                                            variant="primary"
                                            onClick={verifyEmail}
                                        >
                                            {isSendingVerificationEmail ? (
                                                <Loader />
                                            ) : (
                                                'Send Verification Email'
                                            )}
                                        </Button>
                                    </div>
                                </div>
                            </Alert>
                        )}
                    </>
                )}
            </Modal.Body>
            <Modal.Footer>
                <Button
                    className="centricity-btn"
                    variant="outline-primary"
                    onClick={() => updateParentState({ showModal: false, showExport: false })}
                >
                    Cancel
                </Button>
                <Button
                    className=" centricity-btn"
                    variant="primary"
                    disabled={
                        exportFormat === '' &&
                        !selectedDept &&
                        selectedRadioBtn !== 'allFacets' &&
                        selectedRadioBtn !== 'facetType' &&
                        selectedRadioBtn !== 'nodeAndFacet'
                    }
                    onClick={exportData}
                >
                    {isExporting ? <Loader /> : 'Export'}
                </Button>
            </Modal.Footer>
        </>
    );
};

export default ExportHierarchy;
