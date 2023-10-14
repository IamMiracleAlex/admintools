import React from "react";
import {
  FaExternalLinkAlt,
  FaSortAmountDown,
  FaSortAmountDownAlt,
} from "react-icons/fa";
import {
  Tr,
  Th,
  Td,
  Table,
  Thead,
  Tbody,
  Button,
  IconButton,
} from "@chakra-ui/react";
import useSortableClients from "../../../utils/useSortableClients/useSortableClients";
import { formatDate, isClientActive } from "../../../utils";

const SkuClientMapperTable = ({ clients, handleDetailView }) => {
  const { sortedClients, sortBy, sortConfig } = useSortableClients(clients);

  const getIcon = (name) => {
    if (!sortConfig) {
      return <FaSortAmountDown />;
    }
    if (sortConfig.key === name) {
      return sortConfig.direction === "desc" ? (
        <FaSortAmountDown />
      ) : (
        <FaSortAmountDownAlt />
      );
    }
    return <FaSortAmountDown />;
  };

  return (
    <Table variant="striped" colorScheme="lightGray" mr="6" size="sm">
      <Thead>
        <Tr>
          <Th>S/N</Th>
          <Th>Name</Th>
          <Th>
            Mapped SKUs
            <IconButton
              ml="2"
              w={4}
              h={4}
              aria-label="mapped_sku"
              icon={getIcon("mapped_sku")}
              onClick={() => sortBy("mapped_sku")}
            />
          </Th>
          <Th>
            Uploaded SKUs
            <IconButton
              ml="2"
              w={4}
              h={4}
              aria-label="uploaded_sku"
              icon={getIcon("uploaded_sku")}
              onClick={() => sortBy("uploaded_sku")}
            />
          </Th>
          <Th>
            Last Uploaded
            <IconButton
              ml="2"
              w={4}
              h={4}
              aria-label="last_uploaded"
              icon={getIcon("last_uploaded")}
              onClick={() => sortBy("last_uploaded")}
            />
          </Th>
          <Th>
            Last Modified
            <IconButton
              ml="2"
              w={4}
              h={4}
              aria-label="last_modified"
              icon={getIcon("last_modified")}
              onClick={() => sortBy("last_modified")}
            />
          </Th>
          <Th>Status</Th>
          <Th>Actions</Th>
        </Tr>
      </Thead>
      <Tbody>
        {sortedClients.map((client) => {
          return (
            <Tr key={client.id}>
              <Td>{client.id}</Td>
              <Td>
                <Button
                  color="blue.600"
                  fontWeight="medium"
                  fontSize="sm"
                  variant="ghost"
                  onClick={() => handleDetailView(client)}
                >
                  {client.name}
                </Button>
              </Td>
              <Td>{client.mapped_sku}</Td>
              <Td>{client.uploaded_sku}</Td>
              <Td>{formatDate(client.last_uploaded)}</Td>
              <Td>{formatDate(client.last_modified)}</Td>
              <Td>{isClientActive(client.clientuser)}</Td>
              <Td>
                <Button colorScheme="blue" mr="1" size="sm">
                  <FaExternalLinkAlt />
                </Button>
              </Td>
            </Tr>
          );
        })}
      </Tbody>
    </Table>
  );
};

export default SkuClientMapperTable;
