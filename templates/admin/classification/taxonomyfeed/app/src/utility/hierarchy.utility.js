import axios from '../axios';
import {
    deptOptions$,
    categoryOptions$,
    subCategoryOptions$,
    subsetOptions$,
} from '../stream/hierarchy.stream';

export const getDepartment = async () => {
    try {
        const response = await axios.get('/classification/nodes/?level=0');

        if (response) {
            // console.log('respon ', response)
            deptOptions$.next(
                response.data.map((dept) => ({
                    value: dept.id,
                    label: dept.title,
                })),
            );
        }
    } catch (error) {
        console.log('error ', error);
    }
};

export const getCategory = async (deptId) => {
    try {
        const response = await axios.get(`/classification/nodes/${deptId}/treeview/`);

        if (response) {
            categoryOptions$.next(
                response.data.children.map((dept) => ({
                    value: dept.id,
                    label: dept.title,
                })),
            );
        }
    } catch (error) {
        console.log('error ', error);
    }
};

export const getSubCategory = async (categoryId) => {
    try {
        const response = await axios.get(`/classification/nodes/${categoryId}/treeview/`);

        if (response) {
            subCategoryOptions$.next(
                response.data.children.map((dept) => ({
                    value: dept.id,
                    label: dept.title,
                })),
            );
        }
    } catch (error) {
        console.log('error ', error);
    }
};

export const getSubset = async (subCategoryId) => {
    try {
        const response = await axios.get(`/classification/nodes/${subCategoryId}/treeview/`);

        if (response) {
            subsetOptions$.next(
                response.data.children.map((dept) => ({
                    value: dept.id,
                    label: dept.title,
                })),
            );
        }
    } catch (error) {
        console.log('error ', error);
    }
};
