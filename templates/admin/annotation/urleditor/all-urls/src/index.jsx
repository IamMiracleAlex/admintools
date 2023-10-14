import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { QueryParamProvider } from 'use-query-params';
import history from './history';

import 'react-bootstrap/dist/react-bootstrap.min.js';
import 'bootstrap/dist/css/bootstrap.min.css';

import './assets/css/style.css';
import 'vite/dynamic-import-polyfill';

ReactDOM.render(
    <QueryParamProvider history={history}>
        <App />
    </QueryParamProvider>,

    document.getElementById('root'),
);
