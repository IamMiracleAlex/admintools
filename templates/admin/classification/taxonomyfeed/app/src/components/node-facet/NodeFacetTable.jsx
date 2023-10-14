import { format } from 'date-fns';
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { Loader } from '../../common/Loader/Loader';
import { StatusColumn } from '../../common/StatusColumn/StatusColumn';
import { Table } from '../../common/Table/Table';

export const NodeFacetTable = ({ isLoading, data, onRowSelect }) => {
    const [selectedRows, setSelectedRows] = useState([]);

    useEffect(() => {
        onRowSelect(selectedRows);
    }, [selectedRows, onRowSelect]);

    const handleMainCheckboxChange = useCallback(
        (e) => {
            if (!e.target.checked) {
                return setSelectedRows([]);
            }
            return setSelectedRows(
                data.map((i) => ({
                    id: i.id,
                    checked: true,
                })),
            );
        },
        [data],
    );

    const handleCheckboxChange = useCallback(
        (e, id) => {
            if (!e.target.checked) {
                setSelectedRows(selectedRows.filter((e) => e.id !== id));
            } else {
                const newRow = {
                    id,
                    checked: true,
                };
                setSelectedRows((rows) => [...rows, newRow]);
            }
        },
        [selectedRows],
    );

    const columns = useMemo(
        () => [
            {
                Header: <input type="checkbox" onChange={handleMainCheckboxChange} />,
                accessor: 'checkbox',
            },
            {
                Header: 'HIERARCHY (NODES)',
                accessor: 'hierarchy',
            },
            {
                Header: 'Facet Category',
                accessor: 'facet_category',
            },
            {
                Header: 'Facet Value',
                accessor: 'facet_value',
            },
            {
                Header: 'Relationship',
                accessor: 'relationship',
            },
            {
                Header: 'Last Updated',
                accessor: 'last_updated',
            },
            {
                Header: 'Action Performed By',
                accessor: 'user',
            },
        ],
        [handleMainCheckboxChange],
    );

    const tableData = useMemo(
        () =>
            data &&
            data.map((i) => {
                return {
                    checkbox: (
                        <div className="flex justify-content-between align-items-center">
                            <input
                                type="checkbox"
                                id="exampleCheck1"
                                onChange={(e) => handleCheckboxChange(e, i.id)}
                                style={{ marginRight: '14px' }}
                                checked={selectedRows.find((e) => e.id === i.id)?.checked || false}
                            />
                        </div>
                    ),
                    hierarchy: i?.hierarchy,
                    facet_category: i?.facet_category,
                    facet_value: i?.facet_value,
                    relationship: i?.has_facet,
                    last_updated: (
                        <div>
                            <div>{format(Date.parse(i?.updated_at), 'MMM dd, yyyy')}</div>
                            <div>{format(Date.parse(i?.updated_at), 'hh:mm:ss')}</div>
                        </div>
                    ),
                    status: <StatusColumn status={i?.history_type} date={i?.history_date} />,
                    user: i?.history_user,
                };
            }),
        [data, handleCheckboxChange, selectedRows],
    );

    if (isLoading) {
        return (
            <div className="border-wrapper">
                <div className="text-center">
                    <Loader size="lg" />
                </div>
            </div>
        );
    }

    // If no record is found in the database
    if (data && data.length === 0) {
        return (
            <div className="border-wrapper">
                <div className="text-center">
                    <h4> No Node found</h4>
                </div>
            </div>
        );
    }

    return <div>{data && <Table columns={columns} data={tableData} />}</div>;
};
