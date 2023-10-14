import React from 'react';
import { Button, FormControl } from 'react-bootstrap';
import { toggleExpandedForAll } from 'react-sortable-tree';
import { ReactComponent as SearchIcon } from '../../assets/svg/search-icon.svg';
import { ReactComponent as PreviousIcon } from '../../assets/svg/chevron-left.svg';
import { ReactComponent as NextIcon } from '../../assets/svg/chevron-right.svg';
import BulkAssign from '../Modal/BulkAssign';
import { canEdit } from '../../utils/helper';
import {useHistory} from 'react-router-dom';

const HierarchyFilters = ({
    treeData,
    updateState,
    searchFoundCount,
    searchFocusIndex,
    isFetchingHierarchy,
    selectedNodes,
}) => {
    const toggleNodeExpansion = (expanded) => {
        updateState({
            treeData: toggleExpandedForAll({
                treeData,
                expanded,
            }),
        });
    };
    const history = useHistory();

    const handleSkuClick = () => {
        history.push('/sku')
    }

    const handleSearchOnChange = (e) => {
        updateState({ searchString: e.target.value.toUpperCase().trim() });
    };

    const selectPrevMatch = () => {
        updateState({
            searchFocusIndex:
                searchFocusIndex !== null
                    ? (searchFoundCount + searchFocusIndex - 1) % searchFoundCount
                    : searchFoundCount - 1,
        });
    };

    const selectNextMatch = () => {
        updateState({
            searchFocusIndex:
                searchFocusIndex !== null ? (searchFocusIndex + 1) % searchFoundCount : 0,
        });
    };

    return (
        <div className="hierarchy-filters-container">
            <div>
                <Button
                    className="custom-btn-outline-primary mr-2"
                    variant="outline-primary"
                    onClick={() => toggleNodeExpansion(true)}
                >
                    Expand all
                </Button>
                <Button
                    className="custom-btn-outline-primary mr-2"
                    variant="outline-primary"
                    onClick={() => toggleNodeExpansion(false)}
                >
                    Collapse all
                </Button>
                <Button
                    className="custom-btn-primary mr-2"
                    variant="primary"
                    onClick={() => updateState({ showModal: true, showAddFacetCategory: true })}
                    disabled={!canEdit()}
                >
                    Add Facet Category
                </Button>
                <Button
                    className="custom-btn-primary mr-2"
                    variant="primary"
                    onClick={() => updateState({ showModal: true, showAddFacetValue: true })}
                    disabled={!canEdit()}
                >
                    Add Facet Value
                </Button>
                <BulkAssign selectedNodes={selectedNodes} updateState={updateState} />
                {!isFetchingHierarchy && (
                    <Button
                        className="custom-btn-primary mr-2"
                        variant="primary"
                        onClick={() => updateState({ showModal: true, showExport: true })}
                    >
                        Export
                    </Button>
                )}
                <Button
                    className="custom-btn-primary mr-2"
                    variant="primary"
                    onClick={handleSkuClick}
                >
                    SKU Mapping
                </Button>
            </div>
            <div className="d-flex">
                <div className="custom-search-container">
                    <FormControl
                        className="custom-search-field"
                        placeholder="Search"
                        onChange={handleSearchOnChange}
                    />
                    <SearchIcon />
                </div>
                <Button
                    className="ml-2"
                    variant="Link"
                    onClick={selectPrevMatch}
                    disabled={!searchFoundCount}
                >
                    <PreviousIcon />
                </Button>
                <Button variant="Link" onClick={selectNextMatch} disabled={!searchFoundCount}>
                    <NextIcon />
                </Button>
                <p className="search-count">
                    {searchFoundCount > 0 ? searchFocusIndex + 1 : 0} / {searchFoundCount}
                </p>
            </div>
        </div>
    );
};

export default HierarchyFilters;
