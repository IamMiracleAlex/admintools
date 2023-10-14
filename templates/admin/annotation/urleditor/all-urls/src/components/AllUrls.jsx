import React, { useState } from 'react';
import Select from 'react-select/';
import ClientSelect from '../utils/ClientSelect/ClientSelect';
import CountrySelect from '../utils/CountrySelect/CountrySelect';
import { ListFilterOptions, PriorityFilterOptions, UrlTypeOptions } from '../constants/SelectOptions';
import Button from '../utils/Button/Button';
import FormGroupSearch from '../utils/FormGroup/FormGroupSearch/FormGroupSearch';
import './../utils/FormGroup/FormGroupSelect/FormGroupSelect.css';
import AllUrlTable from './AllUrlTable';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

import { useQueryParams, StringParam } from 'use-query-params';

export const AllUrls = () => {
    const [query] = useQueryParams({
        q: StringParam,
    });
    const [status, setStatus] = useState('');
    const [priority, setPriority] = useState('');
    const [client, setClient] = useState('');
    const [country, setCountry] = useState('');
    const [urlType, setUrlType] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [filters, setFilters] = useState({});
    const [startDate, setStartDate] = useState()
    const [endDate, setEndDate] = useState()

    const handleOnChange = dates => {
        const [start, end] = dates;
        setStartDate(start);
        setEndDate(end);
        setFilters({ ...filters, startDate: start, endDate: end })
      };
      
    return (
        <div className="container-fluid mb-5 pb-5 pt-3">
            <div className="all-url-header">
                <div className="d-flex justify-content-between">
                    <h1>ALL URLs</h1>

                    <div className="d-flex">
                        <form
                            className="d-flex"
                            onSubmit={(e) => {
                                e.preventDefault();
                                setFilters({ ...filters, q: searchQuery });
                            }}
                        >
                            <FormGroupSearch
                                name="searchQuery"
                                value={searchQuery || query.q}
                                placeholder="Search by URL"
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                            <Button
                                title="Search"
                                type="submit"
                                className="custom-btn-primary ml-3"
                            />
                        </form>
                    </div>
                </div>

                <div className="filter-row">
                    <div>
                        <div className="font-14">Status</div>
                        <Select
                            value={status}
                            onChange={(data) => {
                                setStatus(data);
                                setFilters({ ...filters, status: data.value });
                            }}
                            options={ListFilterOptions}
                            className="custom-select-container"
                            classNamePrefix="custom-react-select"
                        />
                    </div>

                    <div>
                        <div className="font-14">Priority</div>
                        <Select
                            value={priority}
                            onChange={(data) => {
                                setPriority(data);
                                setFilters({ ...filters, priority: data.value });
                            }}
                            options={PriorityFilterOptions}
                            className="custom-select-container"
                            classNamePrefix="custom-react-select"
                        />
                    </div>

                    <div>
                        <div className="font-14">Client</div>
                        <ClientSelect
                            isFilter
                            value={client}
                            className="w-100"
                            onChange={(data) => {
                                setClient(data);
                                setFilters({ ...filters, client: data.value });
                            }}
                        />
                    </div>

                    <div>
                        <div className="font-14">Country</div>
                        <CountrySelect
                            isFilter
                            value={country}
                            className="w-100"
                            onChange={(data) => {
                                setCountry(data);
                                setFilters({ ...filters, country: data.value });
                            }}
                        />
                    </div>

                    <div>
                        <div className="font-14">URL Type</div>
                        <Select
                            name="urlType"
                            value={urlType}
                            onChange={(data) => {
                                setUrlType(data);
                                setFilters({ ...filters, urlType: data.value });
                            }}
                            options={UrlTypeOptions}
                            className="custom-select-container"
                            classNamePrefix="custom-react-select"
                        />
                    </div>
                    <div>
                        <div className="font-14">Date Range Filter
                        </div>
                        <DatePicker 
                            selected={startDate}
                            startDate={startDate}
                            endDate={endDate}
                            selectsRange
                            onChange={handleOnChange}
                            className="custom-date-container"
                        />
                    </div>

                </div>
            </div>

            <AllUrlTable filtersProps={filters} />
        </div>
    );
};
