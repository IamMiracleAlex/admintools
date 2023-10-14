import axios from '../axios';
import { facetValueOptions$, facetCategoryOptions$ } from '../stream/facet.stream';

export const getFacetValue = async () => {
    try {
        const response = await axios.get('/classification/facet/');

        if (response.status === 200) {
            // console.log('respon ', response)
            const data = response.data.map((facet) => ({
                value: facet.id,
                label: facet.label,
            }));

            facetValueOptions$.next([{ value: '', label: 'All' }, ...data]);
        }
    } catch (error) {
        console.log('error ', error);
    }
};

export const getFacetCategory = async () => {
    try {
        const response = await axios.get('/classification/facet_category/');

        if (response.status === 200) {
            const data = response.data.map((facet) => ({
                value: facet.id,
                label: facet.title,
            }));

            facetCategoryOptions$.next([{ value: '', label: 'All' }, ...data]);
        }
    } catch (error) {
        console.log('error ', error);
    }
};
