import React, {useState, useEffect, useContext} from 'react';
import SkuTable from '../Table';
import MapperFilters from '../MapperFilters';
import {Box, Flex, Text} from '@chakra-ui/react'
import'./index.css'
import ImportSkuMapping from '../Modal/ImportSku';
import HierarchyMappingModal from '../Modal/HierarchyMappingModal';
import NewMapping from '../Modal/NewSku';
import { useQueryParams, StringParam, NumberParam } from 'use-query-params';
import {MapperContext} from '../Mapper';
import {fetchSingleClientSKU} from '../../services';
import NewManufacturer from '../Modal/NewManufacturer';
import CustomAlert from '../Modal/CustomAlert';


const ProxyMapper = ({client, handleDetailView}) => {
    const [query, setQuery] = useQueryParams({
        department: NumberParam,
        category: NumberParam,
        sub_category: NumberParam,
        subset: NumberParam,
        q: StringParam,
        page: NumberParam,
        client_id: NumberParam, 
    });
    const {
        skuMappers,
        setSkuMappers,
        selectedRows,
        setFilteredSkus,
        setSelectedRows
    } = useContext(MapperContext);
    const [searchQuery, setSearchQuery] = useState("")
    const [isLoading, setIsLoading] = useState(false);
    const [headers, setHeaders] = useState([]);
    const [extra, setExtra] = useState({})
    const [alert, setAlert] = useState({
        message: "",
        status: "",
        show: false
    })

    const applySearchFilter = (data, searchString) => {
        const filteredData = data.filter(sku => {
            return Object.keys(sku).some(key => {
                if (typeof(sku[key]) === "string") {
                    return sku[key].toLowerCase().includes(searchString)
                }
            })
        })

        setFilteredSkus(filteredData)
    }

    const handleSearch = (e) => {
        let searchString = e.target.value.toLowerCase();
        setSearchQuery(searchString)
        applySearchFilter(skuMappers, searchString)
    }

    const fetchSkuMappers = async (queryParam) => {
        setIsLoading(true)
        const response = await fetchSingleClientSKU(queryParam);
        if (response.status === 200) {
            const {results, ...extras} = response.data;
            setSkuMappers(results)
            applySearchFilter(results, searchQuery)
            setExtra(extras)
            if (results.length > 0) {
                setHeaders(Object.keys(response.data.results[0]))
            } 
            setIsLoading(false)
        } else {
            setIsLoading(false)
        }
    }

    const refetchOnSuccess = () => {
            fetchSkuMappers(query)
            setSelectedRows([])
        }

    const paginationHandler = (page) => {
        if (!page) {
          return;
        }
        setQuery({ page: page }, "pushIn");
        fetchSkuMappers({ ...query, page:page });
      };

    useEffect(() => {
        if (client) {
            setQuery({...query, client_id: client.id})
        }
        if (query.client_id) {
            fetchSkuMappers(query)
        } else {
            fetchSkuMappers({...query, client_id: client.id});
        }
        return () => {
            setAlert({
                message: "",
                status: "",
                show: false
            })
        }
    }, [skuMappers?.length])

    return (
        <div>
            
            <div className="url-action-container justify-content-end filter-container">
                <MapperFilters handleSearch={handleSearch} />
            </div>
            <CustomAlert 
                open={alert.show} 
                close={() => setAlert({...alert, show: false})} 
                message={alert.message}
                status={alert.status} />
            <Flex className="url-action-container">
                <Box className="d-flex align-vertical">
                    <NewMapping 
                        clientID={client.id} 
                        setAlert={setAlert}
                        refetchData={refetchOnSuccess} 
                    />
                    <Text fontSize="lg">{client.name}</Text>
                </Box>
                <Box>
                    <NewManufacturer setAlert={setAlert} title="Add Manufacturer" refetchData={refetchOnSuccess} />
                    <ImportSkuMapping setAlert={setAlert} refetchData={refetchOnSuccess}/>
                    <HierarchyMappingModal setAlert={setAlert} refetchData={refetchOnSuccess} selectedRows={selectedRows} />
                </Box>
            </Flex>
            <Box className="border-wrapper">
                <SkuTable 
                    setAlert={setAlert}
                    isLoading={isLoading} 
                    refetchData={refetchOnSuccess}
                    extra={extra} 
                    headers={headers} 
                    paginationHandler={paginationHandler} 
                />
            </Box>
        </div>
    );
}
 
export default ProxyMapper;