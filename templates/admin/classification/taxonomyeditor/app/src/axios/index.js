import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000/',
});

instance.interceptors.request.use((config) => {
    config.headers = {
        Authorization: `Token fa55f89280dd1be987a279740c0f8e698c87fca5`,
    };
    return config;
});

export default instance;
