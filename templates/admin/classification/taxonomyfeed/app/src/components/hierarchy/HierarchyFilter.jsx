import React, { useState, useEffect, useCallback } from 'react';
import axios from '../../axios';
import { useSubscription } from '../../hooks/useSubscription';
import { Row, Col, Button } from 'react-bootstrap';
import Select from 'react-select';
import { showNotification } from '../../common/ReactNotification/ReactNotification';
import { FormGroupSearch } from '../../common/FormGroupSearch/FormGroupSearch';
import { SelectDropdown } from '../../common/SelectDropdown/SelectDropdown';
import { SortFilter } from '../../data/Filters';
import {
    deptOptions$,
    categoryOptions$,
    subCategoryOptions$,
    subsetOptions$,
} from '../../stream/hierarchy.stream';
import {
    getDepartment,
    getCategory,
    getSubCategory,
    getSubset,
} from '../../utility/hierarchy.utility';

export const HierarchyFilter = ({ onFilter, rowsSelected }) => {
    const deptOptions = useSubscription(deptOptions$);
    const categoryOptions = useSubscription(categoryOptions$);
    const subCategoryOptions = useSubscription(subCategoryOptions$);
    const subsetOptions = useSubscription(subsetOptions$);
    const [sortBy, setSortBy] = useState('');
    const [department, setDepartment] = useState(null);
    const [category, setCategory] = useState(null);
    const [subCategory, setSubCategory] = useState(null);
    const [subset, setSubset] = useState(null);
    const [search, setSearch] = useState('');
    const [filters, setFilters] = useState(null);
    const [isRestoring, setIsRestoring] = useState(false);

    useEffect(() => {
        getDepartment();
    }, []);

    useEffect(() => {
        if (department?.value) {
            categoryOptions$.next();
            getCategory(department.value);
            setCategory(null);
            setSubCategory(null);
            setSubset(null);
            setFilters((filters) => ({ ...filters, id: department.value }));
        }
    }, [department]);

    useEffect(() => {
        if (category?.value) {
            subCategoryOptions$.next();
            getSubCategory(category.value);
            setSubCategory(null);
            setSubset(null);
            setFilters((filters) => ({ ...filters, id: category.value }));
        }
    }, [category]);

    useEffect(() => {
        if (subCategory?.value) {
            subsetOptions$.next();
            getSubset(subCategory.value);
            setSubset(null);
            setFilters((filters) => ({ ...filters, id: subCategory.value }));
        }
    }, [subCategory]);

    useEffect(() => {
        if (subset?.value) {
            setFilters((filters) => ({ ...filters, id: subset.value }));
        }
    }, [subset]);

    useEffect(() => {
        filters && onFilter(filters);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [filters?.id, filters?.ordering]);

    const restore = useCallback(async () => {
        try {
            setIsRestoring(true);
            const response = await axios.post(`/classification/taxonomy-change-feed/nodes/`, {
                node_ids: rowsSelected,
            });

            if (response) {
                setIsRestoring(false);
                showNotification('Node successfully restored');
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
                    <div className="font-14">Department</div>
                    <Select
                        value={department}
                        onChange={(value) => {
                            setDepartment(value);
                        }}
                        options={deptOptions}
                        isLoading={!deptOptions}
                        className="custom-select-container"
                        classNamePrefix="custom-react-select"
                    />
                </Col>

                {department?.value && (
                    <Col md={2}>
                        <div className="font-14">Category</div>
                        <Select
                            value={category}
                            onChange={(value) => setCategory(value)}
                            options={categoryOptions}
                            isLoading={!categoryOptions}
                            className={'custom-select-container'}
                            classNamePrefix="custom-react-select"
                        />
                    </Col>
                )}

                {category?.value && (
                    <Col md={2}>
                        <div className="font-14">Subcategory</div>
                        <Select
                            value={subCategory}
                            onChange={(value) => setSubCategory(value)}
                            options={subCategoryOptions}
                            isLoading={!subCategoryOptions}
                            className={'custom-select-container'}
                            classNamePrefix="custom-react-select"
                        />
                    </Col>
                )}

                {subCategory?.value && (
                    <Col md={2}>
                        <div className="font-14">Subset</div>
                        <Select
                            value={subset}
                            onChange={(value) => setSubset(value)}
                            options={subsetOptions}
                            isLoading={!subsetOptions}
                            className={'custom-select-container'}
                            classNamePrefix="custom-react-select"
                        />
                    </Col>
                )}

                <Col md={2}>
                    <div className="font-14">&nbsp;</div>
                    <FormGroupSearch value={search} onChange={(e) => setSearch(e.target.value)} />
                </Col>
            </Row>
        </div>
    );
};
