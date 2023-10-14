import React from 'react';
import './NodeHistory.css';

export const NodeHistory = ({ text = '', changedNode = false, status = '' }) => {
    switch (status) {
        case 'Created':
            if (changedNode) {
                return <span className="node-history-badge history-badge-created">{text}</span>;
            } else {
                return text;
            }
        case 'Deleted':
            if (changedNode && text) {
                return <span className="node-history-badge history-badge-deleted">{text}</span>;
            } else {
                return text;
            }
        case 'Changed':
            if (changedNode) {
                return <span className="node-history-badge history-badge-changed">{text}</span>;
            } else {
                return text;
            }
        default:
            return <div>{text}</div>;
    }
};
