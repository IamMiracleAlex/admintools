import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { format } from 'date-fns';
import { Table } from '../../common/Table/Table';
import { StatusColumn } from '../../common/StatusColumn/StatusColumn';
import { Loader } from '../../common/Loader/Loader';
import { NodeHistory } from '../../common/NodeHistory/NodeHistory';

export const FacetTable = ({ isLoading, data, onRowSelect }) => {
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
                Header: 'Facet Category',
                accessor: 'facet_category',
            },
            {
                Header: 'Facet Value',
                accessor: 'facet_value',
            },
            {
                Header: 'Date Created',
                accessor: 'date_created',
            },
            {
                Header: 'Status',
                accessor: 'status',
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
                    facet_category: i?.facet_category,
                    facet_value: (
                        <NodeHistory status={i.history_type} changedNode={true} text={i?.label} />
                    ),
                    date_created: (
                        <div>
                            <div>{format(Date.parse(i?.created_at), 'MMM dd, yyyy')}</div>
                            <div>{format(Date.parse(i?.created_at), 'hh:mm:ss')}</div>
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
                    <h4> No Facet found</h4>
                </div>
            </div>
        );
    }

    return <div>{data && <Table columns={columns} data={tableData} />}</div>;
};
