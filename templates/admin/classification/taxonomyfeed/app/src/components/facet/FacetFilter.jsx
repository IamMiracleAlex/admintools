import React, { useState, useEffect, useCallback } from 'react';
import axios from '../../axios';
import { useSubscription } from '../../hooks/useSubscription';
import { Row, Col, Button } from 'react-bootstrap';
import Select from 'react-select';
import { showNotification } from '../../common/ReactNotification/ReactNotification';
import { FormGroupSearch } from '../../common/FormGroupSearch/FormGroupSearch';
import { SelectDropdown } from '../../common/SelectDropdown/SelectDropdown';
import { SortFilter } from '../../data/Filters';
import { facetValueOptions$, facetCategoryOptions$ } from '../../stream/facet.stream';
import { getFacetValue, getFacetCategory } from '../../utility/facet.utility';

export const FacetFilter = ({ onFilter, rowsSelected }) => {
    const facetValueOptions = useSubscription(facetValueOptions$);
    const facetCategoryOptions = useSubscription(facetCategoryOptions$);
    const [sortBy, setSortBy] = useState('');
    const [facetValue, setFacetValue] = useState(null);
    const [facetCategory, setFacetCategory] = useState(null);
    const [search, setSearch] = useState('');
    const [filters, setFilters] = useState(null);
    const [isRestoring, setIsRestoring] = useState(false);

    useEffect(() => {
        getFacetValue();
        getFacetCategory();
    }, []);

    useEffect(() => {
        filters && onFilter(filters);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [filters?.id, filters?.ordering, filters?.category]);

    const restore = useCallback(async () => {
        try {
            setIsRestoring(true);
            const response = await axios.post(`/classification/taxonomy-change-feed/facets/`, {
                facet_ids: rowsSelected,
            });

            if (response) {
                setIsRestoring(false);
                showNotification('Facet value successfully restored');
            }
        } catch (error) {
            setIsRestoring(false);
            console.log('error ', error);
        }
    }, [rowsSelected]);

    return (
        <div className="filter-section">
            <Row>
                <Col md={2}>
                    <div className="font-14">&nbsp;</div>
                    <Button
                        className="restore-btn"
                        variant="outline-primary"
                        onClick={restore}
                        disabled={rowsSelected.length < 1 || isRestoring}
                    >
                        {isRestoring ? 'Please Wait...' : 'Restore'}
                    </Button>
                </Col>

                <Col md={2}>
                    <div className="font-14">Sort by</div>
                    <Select
                        value={sortBy}
                        onChange={(data) => {
                            setSortBy(data);
                            setFilters((filters) => ({
                                ...filters,
                                ordering: data.value,
                            }));
                        }}
                        options={SortFilter}
                        className="custom-select-container"
                        classNamePrefix="custom-react-select"
                    />
                </Col>

                <Col md={2}>
                    <div className="font-14">Facet Value</div>
                    <Select
                        value={facetValue}
                        onChange={(data) => {
                            setFacetValue(data);
                            setFilters((filters) => ({
                                ...filters,
                                id: data.value,
                            }));
                        }}
                        options={facetValueOptions}
                        isLoading={!facetValueOptions}
                        className="custom-select-container"
                        classNamePrefix="custom-react-select"
                    />
                </Col>

                <Col md={2}>
                    <div className="font-14">Facet Category</div>
                    <Select
                        value={facetCategory}
                        onChange={(data) => {
                            setFacetCategory(data);
                            setFilters((filters) => ({
                                ...filters,
                                category: data.value,
                            }));
                        }}
                        options={facetCategoryOptions}
                        isLoading={!facetCategoryOptions}
                        className="custom-select-container"
                        classNamePrefix="custom-react-select"
                    />
                </Col>

                {/* <Col md={2}>
                    <div className="font-14">&nbsp;</div>
                    <FormGroupSearch value={search} onChange={(e) => setSearch(e.target.value)} />
                </Col> */}
            </Row>
        </div>
    );
};
