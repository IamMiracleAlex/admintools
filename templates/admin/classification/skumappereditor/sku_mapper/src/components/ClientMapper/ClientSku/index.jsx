import React, { useState, useEffect } from "react";
import { BsPlus } from "react-icons/bs";
import { Box, Button, Flex, Text, Select, Spinner } from "@chakra-ui/react";
import axios from "../../../axios";
import ClientSkuTable from "../ClientSkuTable";
import ErrorMessage from "../../../utils/ErrorMessage/ErrorMessage";
import Paginations from "../../../utils/Pagination/Pagination";
import { useQueryParams, NumberParam } from "use-query-params";
import { getErrorMessage } from "../../../utils";
import "./index.css";

const ClientSkuMapper = ({ handleDetailView }) => {
  const [clients, setClients] = useState([]);
  const [pageData, setPageData] = useState(null);
  const [error, setError] = useState({ show: false, message: "" });
  const [query, setQuery] = useQueryParams({
    page: NumberParam,
  });

  const showOptions = {
    size: [10, 20, 40],
    defaultSize: 10,
  };

  useEffect(() => {
    const fetchClientSKU = async () => {
      await fetchPage({ page_limit: showOptions.defaultSize });
    };
    fetchClientSKU();
  }, []);

  const handlePageLimitChange = (e) => {
    fetchPage({ page_limit: e.target.value });
  };

  const fetchPage = async (filters) => {
    try {
      const res = await axios.get("/classification/sku_mappers/clients/", {
        params: { ...filters },
      });

      if (res.status === 200) {
        const { results, ...pageResult } = res.data;
        setClients(res.data.results);
        setPageData(pageResult);
      }
    } catch (err) {
      setError({
        message: getErrorMessage(err),
        show: true,
      });
    }
  };

  const handlePagination = (pageNumber) => {
    if (!pageNumber) {
      return;
    }
    setQuery({ page: pageNumber }, "pushIn");
    fetchPage({ ...query, page: pageNumber });
  };

  return (
    <>
      <Flex className="url-action-container">
        <Box className="d-flex align-vertical">
          <Button
            colorScheme="blue"
            className="btn-rad"
            style={{ marginRight: "15px" }}
          >
            <BsPlus size="1.4em" />
          </Button>
          <Text fontSize="lg">All Clients</Text>
        </Box>
        <Select
          onChange={handlePageLimitChange}
          maxWidth="120px"
          value={pageData && pageData.total_items_on_page}
        >
          {showOptions.size.map((size) => (
            <option key={size} value={size}>
              Show {size}
            </option>
          ))}
        </Select>
      </Flex>
      <ErrorMessage
        show={error.show}
        message={error.message}
        hide={() => setError({ show: false })}
      />
      <Box className="border-wrapper">
        {clients.length === 0 ? (
          <Spinner size="xl" />
        ) : (
          <ClientSkuTable
            clients={clients}
            handleDetailView={handleDetailView}
          />
        )}
      </Box>
      {pageData && (
        <Paginations
          totalPages={pageData?.total_pages}
          paginate={handlePagination}
          current={pageData?.current}
        />
      )}
    </>
  );
};

export default ClientSkuMapper;
