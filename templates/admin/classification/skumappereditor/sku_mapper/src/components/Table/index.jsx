import React, {useState, useEffect, useContext} from 'react'
import {
    Table,
    TableCaption,
    Spinner, 
    Box
  } from "@chakra-ui/react"
import './index.css';
import TableBody from './RowBody';
import TableHeader from './TableHeader';
import {fetchSingleClientSKU} from '../../services';
import {MapperContext} from '../Mapper';
import Pagination from '../../utils/Pagination/Pagination';
import { useQueryParams, StringParam, NumberParam } from 'use-query-params';


const SkuTable = ({headers, setAlert, refetchData, isLoading, extra, paginationHandler}) => {
    
    const {skuMappers, filteredSkus, selectedRows} = useContext(MapperContext)


    return (
        <Box>
            <Table variant="simple" size="sm">
                <TableHeader headers={headers} />            
                {isLoading ? 
                    (
                        <tr style={{marginTop: "50px"}}>
                            <td colSpan={10}>
                                <Spinner size="lg" />
                            </td>
                        </tr>
                    )
                    :skuMappers?.length === 0 ? 
                        (<TableCaption>There is nothing to see here yet...</TableCaption>) 
                        :
                        (<TableBody 
                                selectedRows={selectedRows} 
                                dataSource={filteredSkus}
                                isHeader={false}
                                setAlert={setAlert}
                                refetchData={refetchData} />)
                }
            </Table>
            <Pagination
                totalPages={extra?.total_pages}
                paginate={paginationHandler}
                current={extra?.current}
            />

        </Box>
    )
}

export default SkuTable;