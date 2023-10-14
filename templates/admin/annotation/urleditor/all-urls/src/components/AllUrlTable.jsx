import React, { useState, useEffect, useMemo } from 'react';
import axios from '../axios';
import DateTime from '../utils/TableComponents/DateTime/DateTime';
import URLState from '../utils/TableComponents/URLState/URLState';
import URLStatus from '../utils/TableComponents/URLStatus/URLStatus';
import URLPriority from '../utils/TableComponents/URLPriority/URLPriority';
import URLColumn from '../utils/TableComponents/URLColumn/URLColumn';
import Paginations from '../utils/Pagination/Pagination';
import UrlInfo from './UrlInfo';
import AddUrl from './AddUrl';
import DeleteUrl from './DeleteUrl';
import ResetUrl from './ResetUrl';
import BulkAssign from './BulkAssign';
import AssignUrl from './AssignUrl';
import Loader from '../utils/Loader/Loader';
import InfoIcon from '../assets/svg/info-icon.svg';
import ErrorStateIcon from '../assets/svg/error-state-icon.svg';
import { getErrorMessage, toSelectOptions } from '../utils/helper';
import Table from './AllUrlsTable/Table';
import { useQueryParams, StringParam, NumberParam } from 'use-query-params';

const AllUrlTable = ({ filtersProps }) => {
    const [query, setQuery] = useQueryParams({
        status: StringParam,
        urlType: StringParam,
        priority: NumberParam,
        client: NumberParam,
        country: NumberParam,
        startDate: StringParam,
        endDate: StringParam,
        q: StringParam,
        page: NumberParam,
    });
    const [isLoading, setIsLoading] = useState(false);
    const [showError, setShowError] = useState(false);
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [errorMsg, setErrorMsg] = useState('');
    const [allUrls, setAllUrls] = useState({});
    const [currentRowInfo, setCurrentRowInfo] = useState(null);
    const [selectedRows, setSelectedRows] = useState([]);

    useEffect(() => {
        const { status, priority, client, country, urlType, startDate, endDate, q } = filtersProps;

        let filters = {};
        if (status || status === '') {
            filters.status = status;
        }
        if (priority || priority === '') {
            filters.priority = priority;
        }
        if (client || client === '') {
            filters.client = client;
        }
        if (country || country === '') {
            filters.country = country;
        }
        if (urlType || urlType === '') {
            filters.urlType = urlType;
        }
        if (q || q === '') {
            filters.q = q;
        }
        if (startDate || startDate === '') {
            filters.startDate = startDate;
        }
        if (endDate || endDate === '') {
            filters.endDate = endDate;
        }
        
        if (Object.entries(filters).length > 0) {
            setQuery(filters, 'push');
            fetchAllUrls(filters);
        } else {
            fetchAllUrls(query);
            setQuery(query);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [filtersProps]);

    const openInfoModal = (rowId) => {
        const currentRowInfo = allUrls.results.find(({ id }) => id === rowId);
        setShowInfoModal(true);
        setCurrentRowInfo(currentRowInfo);
    };

    const hideInfoModal = () => {
        setShowInfoModal(true);
        setCurrentRowInfo(null);
    };

    const handleCheckBoxChange = (e, record) => {
        const { id, url, status, priority, countries, clients } = record;
        if (!e.target.checked) {
            setSelectedRows(selectedRows.filter((e) => e.id !== id));
        } else {
            const newObj = {
                id,
                url,
                status,
                priority,
                countries: countries.map(toSelectOptions),
                clients: clients.map(toSelectOptions),
                checked: e.target.checked,
            };
            setSelectedRows([...selectedRows, newObj]);
        }
    };

    const handlePagination = (e) => {
        setQuery({ page: e }, 'pushIn');
        fetchAllUrls({ ...query, page: e });
    };

    const onAssignSuccess = () => {
        setSelectedRows([]);
        fetchAllUrls(query);
    };

    const fetchAllUrls = async (filters) => {
        try {
            setIsLoading(true);
            setShowError(false);

            const response = await axios.get('annotation/all-urls/', {
                params: { ...filters },
            });
            if (response.status === 200) {
                setAllUrls(response.data);
                setIsLoading(false);
                setShowError(false);
            }
        } catch (error) {
            setErrorMsg(getErrorMessage(error));
            setIsLoading(false);
            setShowError(true);
        }
    };

    const tableData = useMemo(
        () =>
            Object.entries(allUrls).length > 0 &&
            allUrls.results.map((record) => ({
                url: (
                    <URLColumn
                        checked={selectedRows.find((e) => e.id === record.id)?.checked || false}
                        record={record}
                        onChange={(e) => handleCheckBoxChange(e, record)}
                    />
                ),
                page_views: record.page_views,
                state: <URLState state={record.state} />,
                last_counted: <DateTime dateToFormat={record.last_counted} />,
                countries: record.countries.map((e) => e.name).join(', '),
                clients: record.clients.map((e) => e.name).join(', '),
                status: <URLStatus status={record.status} />,
                priority: <URLPriority priority={record.priority} />,
                info: (
                    <div className="info-icon-wrapper">
                        <span onClick={() => openInfoModal(record.id)}>
                            <InfoIcon />
                        </span>
                    </div>
                ),
            })),
        [allUrls, selectedRows],
    );

    const handleMainCheckBoxChange = (e) => {
        if (e.target.checked) {
            setSelectedRows(
                allUrls?.results.map((record) => ({
                    id: record.id,
                    url: record.url,
                    status: record.status,
                    priority: record.priority,
                    countries: record.countries.map(toSelectOptions),
                    clients: record.clients.map(toSelectOptions),
                    checked: true,
                })),
            );
        } else {
            setSelectedRows([]);
        }
    };

    const columns = useMemo(
        () => [
            {
                Header: (
                    <div className="flex justify-content-between align-items-center">
                        <input
                            type="checkbox"
                            onChange={handleMainCheckBoxChange}
                            style={{ marginRight: '14px' }}
                        />
                        <span>{query.urlType || 'ALL'} URLs</span>
                    </div>
                ),
                accessor: 'url',
            },
            {
                Header: 'Views',
                accessor: 'page_views',
            },
            {
                Header: 'State',
                accessor: 'state',
            },
            {
                Header: 'Last Counted',
                accessor: 'last_counted',
            },
            {
                Header: 'Country',
                accessor: 'countries',
            },
            {
                Header: 'Client',
                accessor: 'clients',
            },
            {
                Header: 'List',
                accessor: 'status',
            },
            {
                Header: 'Priority',
                accessor: 'priority',
            },
            {
                Header: 'Info',
                accessor: 'info',
            },
        ],
        [allUrls, selectedRows, query],
    );

    const renderTable = () => {
        if (isLoading) {
            return (
                <div className="border-wrapper">
                    <Loader size="lg" />
                </div>
            );
        }
        if (showError) {
            return (
                <div className="border-wrapper">
                    <ErrorStateIcon />
                    <h4 className="py-4">
                        {errorMsg ? errorMsg : 'Something went wrong, Try again!!!'}
                    </h4>
                </div>
            );
        }
        // If no record is found in the database
        if (Object.entries(allUrls).length > 0 && allUrls.results.length === 0) {
            return (
                <div className="border-wrapper">
                    <h4> No URL found</h4>
                </div>
            );
        }

        if (Object.entries(allUrls).length > 0 && allUrls.results.length > 0) {
            return (
                <>
                    <div className="position-relative">
                        <Table columns={columns} data={tableData} />
                        <Paginations
                            totalPages={allUrls?.count}
                            paginate={handlePagination}
                            currentPage={query?.page}
                        />
                    </div>
                    {currentRowInfo && (
                        <UrlInfo
                            show={showInfoModal}
                            onHide={hideInfoModal}
                            info={currentRowInfo}
                        />
                    )}
                </>
            );
        }
    };

    const rowCount =
        Object.entries(allUrls).length > 0 &&
        allUrls.results.length > 0 &&
        `${selectedRows.length} of ${allUrls.results.length} selected`;
    return (
        <>
            <div className="url-action-container">
                <div className="d-flex align-items-center" style={{ minWidth: '35%' }}>
                    <DeleteUrl selectedRows={selectedRows} assignSuccess={onAssignSuccess} />
                    <ResetUrl selectedRows={selectedRows} assignSuccess={onAssignSuccess} />
                    <span className="font-14 text-nowrap">{rowCount}</span>
                </div>
                <div>
                    <BulkAssign selectedRows={selectedRows} assignSuccess={onAssignSuccess} />
                    <AssignUrl selectedRows={selectedRows} assignSuccess={onAssignSuccess} />
                    <AddUrl refreshTable={fetchAllUrls} />
                </div>
            </div>
            {renderTable()}
        </>
    );
};

export default AllUrlTable;
