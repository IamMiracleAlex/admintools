import React, { Component } from 'react';
import axios from '../axios';
import ReactNotification from 'react-notifications-component';
import { Row, Col, Modal } from 'react-bootstrap';
import SortableTree, {
    addNodeUnderParent,
    changeNodeAtPath,
    removeNodeAtPath,
    defaultGetNodeKey as getNodeKey,
} from 'react-sortable-tree';
import HierarchyFilters from './HierarchyFilters/HierarchyFilters';
import NodeEditor from './NodeEditor/NodeEditor';
import DeleteNode from './Modal/DeleteNode';
import AddFacetCategory from './Modal/AddFacetCategory';
import AddFacetValue from './Modal/AddFacetValue';
import ExportHierarchy from './Modal/ExportHierarchy';
import Loader from './Loader/Loader';
import ErrorMessage from './ErrorMessage/ErrorMessage';
import { showNotification } from './ReactNotification/ReactNotification';
import { getErrorMessage, getAllNodesId, canEdit, getAllDepts } from '../utils/helper';

import 'react-sortable-tree/style.css';
import '../assets/css/custom-sortable-tree.css';

class Hierarchy extends Component {
    state = {
        isLoading: false,
        isFetchingFacets: false,
        showModal: false,
        showDelete: false,
        showAddFacetCategory: false,
        showAddFacetValue: false,
        showBulkAssign: false,
        showExport: false,
        refreshFacetCategory: false,
        refreshFacetValue: false,
        selectAll: false,
        selectDepts: false,
        searchString: '',
        searchFocusIndex: 0,
        searchFoundCount: null,
        nodeClicked: null,
        selectedNodes: [],
        treeData: [],
    };

    componentDidMount = () => {
        this.fetchHierarchy();
        sessionStorage.setItem('has_write_access', 'True')
    };

    fetchHierarchy = async () => {
        try {
            this.setState({ isLoading: true });
            const { data } = await axios.get('/classification/nodes/tree/');

            this.setState({ isLoading: false, treeData: data });
        } catch (error) {
            this.setState({
                isLoading: false,
                errorMsg: getErrorMessage(error),
                showError: true,
            });
        }
    };

    fetchNodeFacets = async ({ node, parentNode, path }) => {
        try {
            this.setState({ isFetchingFacets: true });
            const { data } = await axios.get(`/classification/nodes/${node.id}/facets/`);

            const { treeData } = this.state;

            this.setState({
                isFetchingFacets: false,
                nodeFacet: data,
                treeData: changeNodeAtPath({
                    treeData,
                    path: path,
                    getNodeKey,
                    newNode: { ...node, facet_properties: data },
                }),
                nodeClicked: { parentNode, node: { ...node, facet_properties: data }, path },
            });
        } catch (error) {
            this.setState({
                isFetchingFacets: false,
                errorMsg: getErrorMessage(error),
                showError: true,
            });
        }
    };

    hideModal = () => {
        this.setState({
            showModal: false,
            showDelete: false,
            showAddFacetCategory: false,
            showAddFacetValue: false,
        });
    };

    handleStateUpdate = (state) => this.setState({ ...state });

    handleSearchFinishCallback = (matches) => {
        this.setState({
            searchFoundCount: matches.length,
            searchFocusIndex: matches.length > 0 ? this.state.searchFocusIndex % matches.length : 0,
        });
    };

    handleNodeOnClick = (node, e) => {
        const selectedClass = ['rst__rowContents', 'rst__rowLabel', 'rst__rowTitle'];
        if (selectedClass.includes(e.target.className)) {
            if (node.node.id) {
                this.fetchNodeFacets(node);
            } else {
                this.setState({
                    nodeClicked: {
                        parentNode: node.parentNode,
                        node: node.node,
                        path: node.path,
                    },
                });
            }
        }
    };

    addNewDepartment = ({ node, path }) => {
        this.setState({
            treeData: addNodeUnderParent({
                treeData: this.state.treeData,
                getNodeKey,
                newNode: {
                    title: 'NEW NODE',
                    description: '',
                    facet_properties: [],
                    parent: null,
                },
            }).treeData,
            node: { path, node },
        });
    };

    addNodeUnderParent = ({ node, path }) => {
        this.setState({
            treeData: addNodeUnderParent({
                treeData: this.state.treeData,
                parentKey: path[path.length - 1],
                expandParent: true,
                getNodeKey,
                newNode: {
                    title: 'NEW NODE',
                    description: '',
                    facet_properties: [],
                },
            }).treeData,
            node: { path, node },
        });
    };

    deleteNodeAtPath = ({ node, path }) => {
        if (!node.id) {
            return this.setState({
                treeData: removeNodeAtPath({
                    treeData: this.state.treeData,
                    path,
                    getNodeKey,
                }),
                node: {},
            });
        }
        this.setState({
            showModal: true,
            showDelete: true,
            node: { path, node },
        });
    };

    handleInputChange = ({ target }) => {
        const { name, value } = target;
        this.setState((prevState) => ({
            formData: {
                ...prevState.formData,
                [name]: value,
            },
        }));
    };

    // selects all nodes
    handleMainCheckBoxChange = (e) => {
        if (e.target.checked) {
            this.setState({
                selectedNodes: getAllNodesId(this.state.treeData),
                selectAll: true,
                selectDepts: false,

            });
        } else {
            this.setState({ selectedNodes: [], selectAll: false });
        }
    };

    // selects all depts
    handleDeptsCheckBoxChange = (e) => {
        if (e.target.checked) {
            this.setState({
                selectedNodes:  getAllDepts(this.state.treeData),
                selectDepts: true,
                selectAll:false
            });
        } else {
            this.setState({ selectedNodes: [], selectDepts: false });
        }
    };

    // selects a single node
    handleCheckBoxChange = (e, node) => {
        if (!e.target.checked) {
            this.setState({
                selectedNodes: this.state.selectedNodes.filter((e) => e.id !== node.node.id),
            });
        } else {
            this.setState({
                selectedNodes: [
                    ...this.state.selectedNodes,
                    { id: node.node.id, checked: e.target.checked },
                ],
            });
        }
    };

    updateNodeOnMove = async ({ node, nextParentNode }) => {
        const { id, title, description, facet_properties } = node;
        try {
            if (!canEdit()) {
                throw new Error('Oops!! You do not have write access');
            }
            const res = await axios.patch(`classification/nodes/${id}/`, {
                title,
                description,
                facet_properties,
                parent: nextParentNode ? nextParentNode.id : null,
            });
            if (res.status === 200) {
                showNotification('Node Successfully Updated');
            }
        } catch (error) {
            this.setState({
                isLoading: false,
                errorMsg: getErrorMessage(error),
                showError: true,
            });
        }
    };

    render = () => {
        const {
            isLoading,
            isFetchingFacets,
            searchString,
            searchFoundCount,
            searchFocusIndex,
            treeData,
            showModal,
            showDelete,
            showAddFacetCategory,
            showAddFacetValue,
            selectedNodes,
            selectAll,
            selectDepts,
            showExport,
            refreshFacetCategory,
            refreshFacetValue,
            node,
            nodeClicked,
            showError,
            errorMsg,
        } = this.state;

        return (
            <div className="container-fluid main-content">
                <ReactNotification className="custom-notification-container" />
                <HierarchyFilters
                    isFetchingHierarchy={isLoading}
                    updateState={this.handleStateUpdate}
                    treeData={treeData}
                    searchFoundCount={searchFoundCount}
                    searchFocusIndex={searchFocusIndex}
                    selectedNodes={selectedNodes}
                />
                <Row>
                    <Col lg={6} md={12}>
                        <div className="column-container">
                            <div className="hierarchy-wrapper">
                                <div style={{ height: 960 }}>
                                    <ErrorMessage
                                        show={showError}
                                        message={errorMsg}
                                        hide={() => this.setState({ showError: false })}
                                    />
                                    {isLoading ? (
                                        <Loader size="lg" />
                                    ) : (
                                        <>
                                            <div className="select-all-container">
                                                <input
                                                    type="checkbox"
                                                    id="mainCheckbox"
                                                    className="select-all-checkbox"
                                                    checked={selectAll}
                                                    onChange={this.handleMainCheckBoxChange}
                                                />
                                                <label htmlFor="mainCheckbox">Select All</label>
                                                <input
                                                    type="checkbox"
                                                    id="deptsCheckbox"
                                                    className="select-depts-checkbox"
                                                    checked={selectDepts}
                                                    onChange={this.handleDeptsCheckBoxChange}
                                                />
                                                <label htmlFor="deptsCheckbox">Select Depts </label>
                                            </div>
                                            <SortableTree
                                                className="custom-sortable-tree-container"
                                                treeData={treeData}
                                                onChange={(treeData) => this.setState({ treeData })}
                                                searchQuery={searchString}
                                                searchFocusOffset={searchFocusIndex}
                                                searchFinishCallback={
                                                    this.handleSearchFinishCallback
                                                }
                                                rowHeight={55}
                                                onMoveNode={this.updateNodeOnMove}
                                                canDrop={({ nextPath }) => nextPath.length < 5}
                                                onlyExpandSearchedNodes={true}
                                                generateNodeProps={(node) => ({
                                                    onClick: (e) => {
                                                        this.handleNodeOnClick(node, e);
                                                    },
                                                    style:
                                                        node.node === nodeClicked?.node
                                                            ? {
                                                                  borderRadius: 9,
                                                                  border: 'solid 2px #0086c6',
                                                              }
                                                            : null,
                                                    buttons: [
                                                        node.treeIndex === 0 && (
                                                            <button
                                                                onClick={() =>
                                                                    this.addNewDepartment(node)
                                                                }
                                                            >
                                                                Add Dept
                                                            </button>
                                                        ),
                                                        node.path.length < 4 && (
                                                            <button
                                                                onClick={() =>
                                                                    this.addNodeUnderParent(node)
                                                                }
                                                            >
                                                                +
                                                            </button>
                                                        ),
                                                        <button
                                                            onClick={() =>
                                                                this.deleteNodeAtPath(node)
                                                            }
                                                        >
                                                            x
                                                        </button>,
                                                        <input
                                                            type="checkbox"
                                                            id="exampleCheck1"
                                                            style={{ marginRight: '14px' }}
                                                            checked={
                                                                selectedNodes.find(
                                                                    (e) => e.id === node.node.id,
                                                                )?.checked || false
                                                            }
                                                            onChange={(e) =>
                                                                this.handleCheckBoxChange(e, node)
                                                            }
                                                        />,
                                                    ],
                                                })}
                                            />
                                        </>
                                    )}
                                </div>
                            </div>
                        </div>
                    </Col>
                    <Col lg={6} md={12}>
                        <NodeEditor
                            onClickNode={nodeClicked}
                            treeData={treeData}
                            updateParentState={this.handleStateUpdate}
                            refreshFacetCategory={refreshFacetCategory}
                            refreshFacetValue={refreshFacetValue}
                            fetchingFacets={isFetchingFacets}
                        />
                    </Col>
                </Row>
                <Modal
                    className="hierarchy-modal"
                    show={showModal}
                    backdrop="static"
                    onHide={this.hideModal}
                >
                    {showDelete && (
                        <DeleteNode
                            showDelete={showDelete}
                            node={node}
                            treeData={treeData}
                            updateParentState={this.handleStateUpdate}
                        />
                    )}
                    {showAddFacetCategory && (
                        <AddFacetCategory updateParentState={this.handleStateUpdate} />
                    )}
                    {showAddFacetValue && (
                        <AddFacetValue updateParentState={this.handleStateUpdate} />
                    )}
                    {showExport && (
                        <ExportHierarchy
                            treeData={treeData}
                            updateParentState={this.handleStateUpdate}
                            selectedNodes={selectedNodes}
                        />
                    )}
                </Modal>
            </div>
        );
    };
}

export default Hierarchy;
