import React from 'react';
import'./index.css'
import ProxyMapper from './ProxyMapper';

export const MapperContext = React.createContext({
    skuMappers: [],
    setSkuMappers: () => {},
    filteredSkus: [],
    setFilteredSkus: () => {},
    selectedRows: [],
    setSelectedRows: () => {},
});

const Mapper = ({client, handleDetailView}) => {

    const [skuMappers, setSkuMappers] = React.useState([])
    const [selectedRows, setSelectedRows] = React.useState([]);
    const [filteredSkus, setFilteredSkus] = React.useState([]);

    return (
        <MapperContext.Provider
            value={{
                skuMappers,
                setSkuMappers,
                selectedRows,
                setSelectedRows,
                filteredSkus,
                setFilteredSkus
            }}>
            <ProxyMapper client={client} handleDetailView={handleDetailView} />
        </MapperContext.Provider>
    );
}
 
export default Mapper;
