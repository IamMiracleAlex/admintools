import React, { Component } from 'react';
import axios from '../axios';
import Button from '../utils/Button/Button';
import FormGroupSelect from '../utils/FormGroup/FormGroupSelect/FormGroupSelect';
import Modal from '../utils/Modal/Modal';
import Loader from '../utils/Loader/Loader';
import ErrorMessage from '../utils/ErrorMessage/ErrorMessage';
import { ListOptions, PriorityOptions } from '../constants/SelectOptions';
import { getErrorMessage } from '../utils/helper';

const initialFormData = { priority: '', status: '', clients: '', countries: '' };

class BulkAssign extends Component {
    state = {
        show: false,
        isSaving: false,
        clientsData: [],
        countriesData: [],
        formData: { ...initialFormData },
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
                    formData: { ...initialFormData },
                    success: {
                        show: true,
                        message: `You have successfully updated ${this.props.selectedRows.length} URLs`,
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
        this.setState({
            show: true,
            success: null,
        });
    };

    hideModal = () => this.setState({ show: false, formData: { ...initialFormData } });

    handleSelectChange = (value, data) => {
        this.setState((prevState) => ({
            formData: { ...prevState.formData, [data.name]: value },
        }));
    };

    handleSubmit = (e) => {
        e.preventDefault();
        const { status, priority, clients, countries } = this.state.formData;
        const newFormData = this.props.selectedRows.map((row) => ({
            url: row.id,
            status: status.value,
            priority: priority.value,
            ...(countries && { countries: countries.map(({ value }) => value) }),
            ...(clients && { clients: clients.map(({ value }) => value) }),
        }));

        console.log('new ', newFormData);
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
                    title="Bulk Assign"
                    className="custom-btn-primary w-160 mr-3"
                    onClick={this.showModal}
                    disabled={selectedRows.length < 1}
                />
                {show && (
                    <Modal
                        show={show}
                        onHide={this.hideModal}
                        title="Bulk Assign"
                        backdrop="static"
                        success={success}
                        className="bulk-assign-modal"
                    >
                        <ErrorMessage
                            show={showError}
                            message={errorMsg}
                            hide={() => this.setState({ showError: false })}
                        />

                        <form onSubmit={this.handleSubmit}>
                            <div className="bulk-assign-container">
                                <div className="d-flex mb-3">
                                    <p>URLs Selected: </p>
                                    <p>{selectedRows.length}</p>
                                </div>
                                <div>
                                    <p>
                                        Priority <span className="text-danger pl-1">*</span>
                                    </p>
                                    <FormGroupSelect
                                        className="w-100"
                                        name="priority"
                                        value={formData.priority}
                                        onChange={(e, data) => this.handleSelectChange(e, data)}
                                        options={PriorityOptions}
                                    />
                                </div>

                                <div>
                                    <p>
                                        Status<span className="text-danger pl-1">*</span>
                                    </p>
                                    <FormGroupSelect
                                        name="status"
                                        className="w-100"
                                        value={formData.status}
                                        onChange={(e, data) => this.handleSelectChange(e, data)}
                                        options={ListOptions}
                                    />
                                </div>

                                <div>
                                    <p>Client</p>
                                    <FormGroupSelect
                                        isMulti
                                        name="clients"
                                        value={formData.clients}
                                        ƒ
                                        className="w-100"
                                        options={clientsData}
                                        isLoading={!clientsData}
                                        onChange={(e, data) => this.handleSelectChange(e, data)}
                                    />
                                </div>

                                <div>
                                    <p>Country</p>
                                    <FormGroupSelect
                                        isMulti
                                        name="countries"
                                        value={formData.countries}
                                        options={countriesData}
                                        isLoading={!countriesData}
                                        className="w-100"
                                        onChange={(e, data) => this.handleSelectChange(e, data)}
                                    />
                                </div>
                            </div>

                            <div className="float-right mt-4 mb-3">
                                <Button
                                    title="Cancel"
                                    className="custom-btn-primary-outline rounded-border mr-3"
                                    onClick={this.hideModal}
                                />
                                <Button
                                    type="submit"
                                    title={isSaving ? <Loader /> : 'Save'}
                                    disabled={!formData.status || !formData.priority || isSaving}
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

export default BulkAssign;
