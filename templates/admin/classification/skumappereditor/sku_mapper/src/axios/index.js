import axios from 'axios';

const instance = axios.create({
    baseURL: `${localStorage.getItem('BASE_URL')}`,
});

instance.interceptors.request.use((config) => {
    config.headers = {
        Authorization: `Token ${sessionStorage.getItem('hierarchy_session')}`,
    };
    return config;
});

export default instance;
