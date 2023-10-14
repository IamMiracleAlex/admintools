import React, { Component } from 'react';
import axios from '../axios';
import Button from '../utils/Button/Button';
import FormGroupSelect from '../utils/FormGroup/FormGroupSelect/FormGroupSelect';
import Modal from '../utils/Modal/Modal';
import Loader from '../utils/Loader/Loader';
import ErrorMessage from '../utils/ErrorMessage/ErrorMessage';
import { ListOptions, PriorityOptions } from '../constants/SelectOptions';
import { getErrorMessage, defaultPriorityValue, defaultStatusValue } from '../utils/helper';

class AssignUrl extends Component {
    state = {
        show: false,
        isSaving: false,
        clientsData: [],
        countriesData: [],
        formData: [],
    };

    componentDidMount = () => {
        this.getClientsData();
        this.getCountriesData();
    };

    getCountriesData = async () => {
        try {
            const res = await axios.get('/annotation/countries/');

            if (res.status === 200) {
                const countriesData = res.data.map(({ id, name }) => ({
                    value: id,
                    label: name,
                }));
                this.setState({ countriesData });
            }
        } catch (error) {
            this.setState({ countriesData: [] });
        }
    };

    getClientsData = async () => {
        try {
            const res = await axios.get('/annotation/clients/');

            if (res.status === 200) {
                const clientsData = res.data.map(({ id, name }) => ({
                    value: id,
                    label: name,
                }));
                this.setState({ clientsData });
            }
        } catch (error) {
            this.setState({ clientsData: [] });
        }
    };

    assignUrl = async (data) => {
        try {
            this.setState({ isSaving: true, showError: false });
            const res = await axios.post('/annotation/urls/edit/', data);
            if (res.status === 200) {
                this.setState({
                    isSaving: false,
                    success: {
                        show: true,
                        message: 'URL successfully updated',
                    },
                });
                this.props.assignSuccess();
            }
        } catch (error) {
            this.setState({
                isSaving: false,
                errorMsg: getErrorMessage(error),
                showError: true,
            });
        }
    };

    showModal = () => {
        const formData = this.props.selectedRows;
        this.setState({
            show: true,
            success: null,
            formData,
        });
    };

    hideModal = () => this.setState({ show: false, formData: [] });

    handleSelectChange = (value, data, index) => {
        const newFormData = this.state.formData;
        newFormData[index] = { ...newFormData[index], [data.name]: value };

        this.setState({ formData: newFormData });
    };

    handleMultiSelectChange = (value, data, index) => {
        if (value === null) {
            value = [];
        }
        const newFormData = this.state.formData;
        newFormData[index] = { ...newFormData[index], [data.name]: value };

        this.setState({ formData: newFormData });
    };

    handleSubmit = (e) => {
        e.preventDefault();

        const newFormData = this.state.formData.map((data) => ({
            url: data.id,
            status: data.status?.value || data.status,
            priority: data.priority.value || data.priority,
            countries: data.countries.map(({ value }) => value) || data.countries,
            clients: data.clients.map(({ value }) => value) || data.clients,
        }));
        
        this.assignUrl(newFormData);
    };

    render() {
        const {
            show,
            isSaving,
            showError,
            errorMsg,
            clientsData,
            countriesData,
            formData,
            success,
        } = this.state;
        const { selectedRows } = this.props;
        return (
            <>
                <Button
                    title="Edit/Assign"
                    className="custom-btn-primary w-160 mr-3"
                    onClick={this.showModal}
                    disabled={selectedRows.length < 1}
                />
                {show && (
                    <Modal
                        show={show}
                        onHide={this.hideModal}
                        title="Assign"
                        backdrop="static"
                        success={success}
                        className="assign-url-modal"
                    >
                        <ErrorMessage
                            show={showError}
                            message={errorMsg}
                            hide={() => this.setState({ showError: false })}
                        />

                        <form onSubmit={this.handleSubmit}>
                            {selectedRows.map((row, index) => {
                                return (
                                    <div key={row.id} className="assign-url-row">
                                        <div>
                                            <div>&nbsp;</div>
                                            <a
                                                href={row.url}
                                                target="_blank"
                                                rel="noreferrer"
                                                className="text-break"
                                            >
                                                {row.url.length > 40
                                                    ? row.url.slice(0, 40) + '....'
                                                    : row.url}
                                            </a>
                                        </div>

                                        <div>
                                            <p>Priority</p>
                                            <FormGroupSelect
                                                className="w-100"
                                                name="priority"
                                                value={formData.priority}
                                                defaultValue={defaultPriorityValue(
                                                    Number(row.priority),
                                                )}
                                                onChange={(e, data) =>
                                                    this.handleSelectChange(e, data, index)
                                                }
                                                options={PriorityOptions}
                                            />
                                        </div>

                                        <div>
                                            <p>Status</p>
                                            <FormGroupSelect
                                                name="status"
                                                className="w-100"
                                                value={formData.status}
                                                defaultValue={defaultStatusValue(row.status)}
                                                onChange={(e, data) =>
                                                    this.handleSelectChange(e, data, index)
                                                }
                                                options={ListOptions}
                                            />
                                        </div>

                                        <div>
                                            <p>Client</p>
                                            <FormGroupSelect
                                                isMulti
                                                name="clients"
                                                value={formData.clients}
                                                defaultValue={row.clients}
                                                className="w-100"
                                                options={clientsData}
                                                isLoading={!clientsData}
                                                onChange={(e, data) =>
                                                    this.handleMultiSelectChange(e, data, index)
                                                }
                                            />
                                        </div>

                                        <div>
                                            <p>Country</p>
                                            <FormGroupSelect
                                                isMulti
                                                name="countries"
                                                value={formData.countries}
                                                defaultValue={row.countries}
                                                options={countriesData}
                                                isLoading={!countriesData}
                                                className="w-100"
                                                onChange={(e, data) =>
                                                    this.handleMultiSelectChange(e, data, index)
                                                }
                                            />
                                        </div>
                                    </div>
                                );
                            })}

                            <div className="float-right mt-4 mb-3">
                                <Button
                                    title="Cancel"
                                    className="custom-btn-primary-outline rounded-border mr-3"
                                    onClick={this.hideModal}
                                />
                                <Button
                                    type="submit"
                                    title={isSaving ? <Loader /> : 'Save'}
                                    disabled={isSaving}
                                    className="custom-btn-primary rounded-border"
                                />
                            </div>
                        </form>
                    </Modal>
                )}
            </>
        );
    }
}

export default AssignUrl;
