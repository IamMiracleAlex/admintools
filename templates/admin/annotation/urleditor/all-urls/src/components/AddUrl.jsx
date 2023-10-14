import React, { Component } from 'react';
import axios from '../axios';
import { Col, Row } from 'react-bootstrap';
import Button from '../utils/Button/Button';
import FormGroupInput from '../utils/FormGroup/FormGroupInput/FormGroupInput';
import FormGroupSelect from '../utils/FormGroup/FormGroupSelect/FormGroupSelect';
import Modal from '../utils/Modal/Modal';
import CountrySelect from '../utils/CountrySelect/CountrySelect';
import ClientSelect from '../utils/ClientSelect/ClientSelect';
import Loader from '../utils/Loader/Loader';
import ErrorMessage from '../utils/ErrorMessage/ErrorMessage';
import { ListOptions, PriorityOptions } from '../constants/SelectOptions';
import AddIcon from '../assets/svg/add-icon.svg';
import { getErrorMessage } from '../utils/helper';

const initialFormData = {
    url: '',
    page_views: '',
    status: '',
};
class AddUrl extends Component {
    state = {
        show: false,
        isSaving: false,
        formData: initialFormData,
    };

    addUrl = async (data) => {
        try {
            this.setState({ isSaving: true, showError: false });
            const res = await axios.post('/annotation/add-url/', {
                ...data,
            });
            if (res.status === 201) {
                this.setState({
                    isSaving: false,
                    success: {
                        show: true,
                        message: 'You have successfully added a new URL',
                    },
                });
                this.props.refreshTable();
            }
        } catch (error) {
            this.setState({
                isSaving: false,
                errorMsg: getErrorMessage(error),
                showError: true,
            });
        }
    };

    toggleModal = () => {
        this.setState((prevState) => ({
            show: !prevState.show,
            success: null,
            formData: initialFormData,
        }));
    };

    handleInputChange = ({ target }) => {
        this.setState((prevState) => ({
            formData: {
                ...prevState.formData,
                [target.name]: target.value,
            },
        }));
    };

    handleSelectChange = (value, data) => {
        this.setState((prevState) => ({
            formData: {
                ...prevState.formData,
                [data.name]: value,
            },
        }));
    };

    handleSubmit = (e) => {
        e.preventDefault();

        const { formData } = this.state;
        const { status, priority, countries, clients } = formData;
        if (status === '') {
            this.setState((prevState) => ({
                errors: {
                    ...prevState.errors,
                    status: true,
                },
            }));
        } else {
            const data = {
                ...formData,
                status: status?.value,
                ...(priority && { priority: priority.value }),
                ...(countries && { countries: countries.map(({ value }) => value) }),
                ...(clients && { clients: clients.map(({ value }) => value) }),
            };
            this.addUrl(data);
        }
    };

    render() {
        const { show, isSaving, errors, showError, errorMsg, formData, success } = this.state;
        return (
            <>
                <Button
                    title={
                        <>
                            <AddIcon />
                            <span className="ml-2" style={{ verticalAlign: 'middle' }}>
                                Add URLs
                            </span>
                        </>
                    }
                    className="custom-btn-primary w-160"
                    onClick={this.toggleModal}
                />
                <Modal
                    show={show}
                    onHide={this.toggleModal}
                    title="Add URL"
                    backdrop="static"
                    success={success}
                    className="add-url-modal"
                >
                    <ErrorMessage
                        show={showError}
                        message={errorMsg}
                        hide={() => this.setState({ showError: false })}
                    />
                    <form onSubmit={this.handleSubmit}>
                        <FormGroupInput
                            label="URL"
                            name="url"
                            className="url-input"
                            value={formData.url}
                            onChange={this.handleInputChange}
                            required
                        />
                        <Row>
                            <Col md={6}>
                                <FormGroupInput
                                    type="number"
                                    label="Page Views"
                                    name="page_views"
                                    value={formData.page_views}
                                    onChange={this.handleInputChange}
                                    required
                                />
                                <ClientSelect
                                    label="Client"
                                    isMulti
                                    name="clients"
                                    value={formData.clients}
                                    onChange={this.handleSelectChange}
                                />
                                <FormGroupSelect
                                    label="Priority"
                                    name="priority"
                                    value={formData.priority}
                                    onChange={this.handleSelectChange}
                                    options={PriorityOptions}
                                />
                            </Col>
                            <Col md={6}>
                                <FormGroupSelect
                                    label="Status"
                                    name="status"
                                    value={formData.status}
                                    onChange={this.handleSelectChange}
                                    options={ListOptions}
                                    required
                                    error={errors?.status}
                                />
                                <CountrySelect
                                    label="Country"
                                    isMulti
                                    name="countries"
                                    value={formData.countries}
                                    onChange={this.handleSelectChange}
                                />
                            </Col>
                        </Row>
                        <div className="float-right mt-4 mb-3">
                            <Button
                                title="Cancel"
                                className="custom-btn-primary-outline rounded-border mr-3"
                                onClick={this.toggleModal}
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
            </>
        );
    }
}

export default AddUrl;
