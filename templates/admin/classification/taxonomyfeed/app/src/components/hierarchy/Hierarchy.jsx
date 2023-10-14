import React, { useState, useEffect, useCallback } from 'react';
import axios from '../../axios';
import Pagination from '../../common/Pagination/Pagination';
import { HierarchyFilter } from './HierarchyFilter';
import { HierarchyTable } from './HierarchyTable';

export const Hierarchy = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [record, setRecord] = useState(null);
    const [filters, setFilters] = useState(null);
    const [page, setPage] = useState(1);
    const [rowsSelected, setRowsSelected] = useState([]);

    const getNode = useCallback(async () => {
        try {
            setIsLoading(true);
            const response = await axios.get(`/classification/taxonomy-change-feed/nodes/`, {
                params: filters,
            });

            if (response) {
                setRecord(response.data);
                setIsLoading(false);
            }
        } catch (error) {
            setIsLoading(false);
        }
    }, [filters]);

    useEffect(() => {
        getNode();
    }, [getNode]);

    const handleFilter = useCallback((filter) => {
        setFilters({ ...filter });
        setPage(1);
    }, []);

    const handleRowSelect = useCallback((data) => {
        setRowsSelected(data?.map((i) => i.id));
    }, []);

    const handlePagination = useCallback((e) => {
        setPage(e);
        setFilters((filters) => ({ ...filters, page: e }));
    }, []);

    return (
        <>
            <HierarchyFilter onFilter={handleFilter} rowsSelected={rowsSelected} />

            <HierarchyTable
                isLoading={isLoading}
                data={record?.results}
                onRowSelect={handleRowSelect}
            />

            {record && Object.entries(record).length > 0 && (
                <Pagination
                    totalPages={record.count}
                    paginate={handlePagination}
                    currentPage={page}
                />
            )}
        </>
    );
};
