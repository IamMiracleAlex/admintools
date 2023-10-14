import React, { useContext, useEffect, useState } from "react";
import { Table, Thead, Tbody, Tr, Th, Td } from "@chakra-ui/table";
import { IoMdOpen } from "react-icons/io";
import Icon from "@chakra-ui/icon";
import { HStack, Link, Spacer, Text, VStack } from "@chakra-ui/layout";
import { Button } from "@chakra-ui/button";
import { Progress } from "@chakra-ui/progress";
import { Heading } from "@chakra-ui/layout";
import { AppContext } from "../../context/AppContext";
import axios from "../axios";
import { useToast } from "@chakra-ui/react";
import { organizeSubscription } from "../../utils/normalise";

const ClientsTable = () => {
  const toast = useToast();
  const { path, client } = useContext(AppContext);
  const [currentPath, setCurrentPath] = path;
  const [selectedClient, setSelectedClient] = client;
  const [clients, setClients] = useState([]);

  const openClientDetails = async (client) => {
    setCurrentPath(`/${client.name}`);
    setSelectedClient(client);

  try{
    const pendingSubscriptions = await axios.get(`api/subscriptions/${client.id}/?status=inactive`)
    const activeSubscriptions = await axios.get(`api/subscriptions/${client.id}/?status=approved`)
    setSelectedClient({
      ...client,
      pendingSubscriptions: organizeSubscription(pendingSubscriptions.data),
      activeSubscriptions: organizeSubscription(activeSubscriptions.data),
    });
     
    }catch(err){
       toast({
         title: `Error Fetching Clients`,
         status: "error",
         isClosable: true,
         position: "top-right",
       });
    }
  }
    

  useEffect(() => {
    axios
      .get("/annotation/clients/")
      .then((res) => {
        setClients(res.data);
      })
      .catch((err) => {
        toast({
          title: `Error Fetching Clients`,
          status: "error",
          isClosable: true,
          position: "top-right",
        });
      });
  }, []);

  const clientRows = clients.map((client) => {
    const { name, status, startDate, endDate } = client;
    const color = status === "active" ? "#3CC13B" : "#F03738";
    const background = status === "active" ? "#EBF9EB" : "#FEEBEB";
    const borderColor = status === "active" ? "#9EE09D" : "#F89B9C";
    return (
      <Tr key={name}>
        <Td>{name}</Td>
        <Td>
          {status === "active" && (
            <>
              <Progress
                borderRadius="10"
                background="#E5E5E5"
                colorScheme="blue"
                size="sm"
                value={20}
              />
              <HStack>
                <Text color="#808080" mt="2" fontSize="xs">
                  {startDate}
                </Text>
                <Spacer />
                <Text mt="2" fontSize="xs">
                  {endDate}
                </Text>
              </HStack>
            </>
          )}
        </Td>
        <Td>
          <Button
            size="xs"
            border="1px"
            color={color}
            background={background}
            borderColor={borderColor}
          >
            {status}
          </Button>
        </Td>
        <Td>
          <Link
            onClick={() => {
              openClientDetails(client);
            }}
          >
            <Text color="grey" _hover={{ color: "#3E66FB" }}>
              <Icon as={IoMdOpen} />
              Open
            </Text>
          </Link>
        </Td>
      </Tr>
    );
  });

  return currentPath !== "/clients" ? (
    <></>
  ) : (
    <>
      <header>
        <Heading as="h1" size="md">
          Client Subscriptions
        </Heading>
      </header>
      <Table mt="12" variant="simple">
        <Thead background="#F9FAFA">
          <Tr>
            <Th>Client</Th>
            <Th>Duration</Th>
            <Th>Status </Th>
            <Th>Action </Th>
          </Tr>
        </Thead>
        <Tbody>{clientRows}</Tbody>
      </Table>
    </>
  );
};

export default ClientsTable;
