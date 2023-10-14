export const getErrorMessage = (error) => {
    const { response } = error;
    if (response?.data.detail) {
        return response.data.detail;
    } else if (response?.data?.non_field_errors) {
        return response.data.non_field_errors;
    } else if (response?.statusText) {
        return `${response?.status}: ${response.statusText}`;
    } else if (error?.message) {
        return error.message;
    } else {
        return `${response?.status}: Something went wrong, Try Again!`;
    }
};

export const getAllNodesId = (treeData) => {
    const allNodes = [];
    treeData.forEach((level1) => {
        allNodes.push({ id: level1.id, checked: true });
        level1.children.forEach((level2) => {
            allNodes.push({ id: level2.id, checked: true });
            level2.children.forEach((level3) => {
                allNodes.push({ id: level3.id, checked: true });
                level3.children.forEach((level4) => {
                    allNodes.push({ id: level4.id, checked: true });
                });
            });
        });
    });
    return allNodes;
};

export const getAllDepts = (treeData) => {
    const allDepts = [];
    treeData.forEach((level1) => {
        allDepts.push({ id: level1.id, checked: true });
    });
    return allDepts;
};

export const canEdit = () => {
    return sessionStorage.getItem('has_write_access') === 'True' ? true : false;
};

export const convertToCSV = (objArray) => {
    const array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
    let str = '';

    for (let i = 0; i < array.length; i++) {
        let line = '';
        for (let index in array[i]) {
            if (line !== '') line += ',';

            line += array[i][index];
        }

        str += line + '\r\n';
    }

    return str;
};

export const exportCSVFile = (headers, items, fileName) => {
    if (headers) {
        items.unshift(headers);
    }

    const jsonObject = JSON.stringify(items);
    const csv = convertToCSV(jsonObject);
    const exportedFilename = fileName + '.csv';

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    if (navigator.msSaveBlob) {
        // IE 10+
        navigator.msSaveBlob(blob, exportedFilename);
    } else {
        const link = document.createElement('a');
        if (link.download !== undefined) {
            // feature detection
            // Browsers that support HTML5 download attribute
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', exportedFilename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
};
