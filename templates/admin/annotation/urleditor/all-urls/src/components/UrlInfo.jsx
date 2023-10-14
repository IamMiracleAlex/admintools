import React from 'react';
import { Col, Row } from 'react-bootstrap';
import Button from '../utils/Button/Button';
import Modal from '../utils/Modal/Modal';

const UrlInfoRow = ({ name, value }) => (
    <div className="url-info-row">
        <span>{name}:</span>
        <span className="pl-2 text-right">{value}</span>
    </div>
);

const UrlInfo = ({ show, onHide, info }) => {
    return (
        <Modal show={show} onHide={onHide} title="URL Info">
            <div className="url-info-wrapper">
                <div className="url-info-container">
                    <div className="url-info-row">
                        <span>URL:</span>
                        <a href={info.url} target="_blank" rel="noreferrer" className="ml-2">
                            {info.url}
                        </a>
                    </div>
                    <Row>
                        <Col md={6}>
                            <UrlInfoRow name="Known" value={info.known.toString()} />
                            <UrlInfoRow
                                name="Country"
                                value={info.countries.map((e) => e.name).join(', ')}
                            />
                            <UrlInfoRow
                                name="Clients"
                                value={info.clients.map((e) => e.name).join(', ')}
                            />
                            <UrlInfoRow name="Events" value={info.events} />
                            <UrlInfoRow
                                name="Required Annotations"
                                value={info.required_annotations}
                            />
                        </Col>

                        <Col md={6}>
                            <UrlInfoRow name="Page Views" value={info.page_views} />
                            <UrlInfoRow name="Status" value={info.status} />
                            <UrlInfoRow
                                name="Annotators Assigned"
                                value={info.annotators_assigned}
                            />
                            <UrlInfoRow
                                name="Archive Attempt Count"
                                value={info.archive_attempt_count}
                            />
                        </Col>
                    </Row>
                    <div className="url-info-row mt-3">
                        <span>Archived URL:</span>
                        <a
                            href={info.archived_url}
                            target="_blank"
                            rel="noreferrer"
                            className="ml-2 text-break"
                        >
                            {info.archived_url}
                        </a>
                    </div>
                </div>

                <Button
                    title="Done"
                    className="custom-btn-primary rounded-border mb-2"
                    onClick={onHide}
                />
            </div>
        </Modal>
    );
};

export default UrlInfo;
