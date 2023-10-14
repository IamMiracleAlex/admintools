import http from '../axios';


export const fetchSingleClientSKU = async (query_params) => {
    const response = await http.get('/classification/sku_mappers/single_client_sku/', {
        params: {...query_params},
    });
    return response;
}

export const importSKU = async (fileData) => {
    const response = await http.post('/classification/sku_mappers/import_sku/', fileData)
    return response;
}

export const deleteSKU = async (sku_id) => {
    const response = await http.delete(`/classification/sku_mappers/${sku_id}/`);
    return response;
}

export const fetchNodeSimpleList = async (queryParam) => {
    const response = await http.get('/classification/nodes/simple_list/', {
        params: {...queryParam},
    });
    return response;
}

export const mapToHierarchy = async (payload) => {
    const response = await http.post('/classification/sku_mappers/map_to_hierarchy/', payload);
    return response;
}

export const fetchManufacturers = async (queryParams) => {
    const response = await http.get('/classification/manufacturers/', {
        params: {...queryParams}
    });
    return response;
}

export const createManufacturer = async (payload) => {
    const response = await http.post('classification/manufacturers/', payload);
    return response;
}

export const submitSkuData = async (payload) => {
    const response = await http.post('classification/sku_mappers/', payload);
    return response;
}
