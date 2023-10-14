export const getErrorMessage = (errObj) => {
    const errResponse = errObj.response;
    const errorMessage = errResponse?.data?.detail
        ? errObj.detail
        : 'Something went Wrong, Please try again';
    return errorMessage;
};

export const defaultPriorityValue = (value) => {
    switch (value) {
        case 1:
            return { value: 1, label: 'High' };
        case 2:
            return { value: 2, label: 'Medium' };
        case 3:
            return { value: 3, label: 'Low' };
        default:
            break;
    }
};

export const defaultStatusValue = (value) => {
    switch (value) {
        case 'green':
            return { value: 'green', label: 'Green' };
        case 'amber':
            return { value: 'amber', label: 'Amber' };
        case 'red':
            return { value: 'red', label: 'Red' };
        default:
            break;
    }
};

export const toSelectOptions = (e) => {
    return {
        value: e.id,
        label: e.name,
    };
};
