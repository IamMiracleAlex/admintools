import React from 'react';
import { store } from 'react-notifications-component';
import 'react-notifications-component/dist/theme.css';
import './ReactNotification.css';

const ReactNotification = ({ message }) => {
    return (
        <div className={`custom-notification-text-container custom-notification-success`}>
            <p>
                {message} <span>x</span>
            </p>
        </div>
    );
};

export const showNotification = (message) =>
    store.addNotification({
        container: 'top-left',
        animationIn: ['animated', 'fadeIn'],
        animationOut: ['animated', 'fadeOut'],
        type: 'success',
        dismiss: {
            duration: 10000,
        },
        content: <ReactNotification message={message} />,
    });
