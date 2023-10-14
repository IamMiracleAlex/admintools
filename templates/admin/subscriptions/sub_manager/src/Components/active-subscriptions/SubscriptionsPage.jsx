import { Button } from "@chakra-ui/button";
import {
  AccordionButton,
  AccordionItem,
  AccordionIcon,
  AccordionPanel,
  Accordion,
} from "@chakra-ui/accordion";
import { ArrowBackIcon } from "@chakra-ui/icons";
import { Box, Text, Flex, Spacer, Heading } from "@chakra-ui/layout";
import React, { useContext } from "react";
import SubscriptionsAccordion from "./SubscriptionAccordion";
import TaxonomyAccordion from "./Taxonomy";
import { useState } from "react";
import { Select, Icon } from "@chakra-ui/react";
import { HiPencil } from "react-icons/hi";
import { AppContext } from "../../context/AppContext";
import AddSubscriptionModal from "./AddingSubscriptionModal";

const ActiveSubscriptions = () => {
  const { path, client } = useContext(AppContext);
  const [currentPath, setCurrentPath] = path;
  const [clientDetails] = client;
  const { activeSubscriptions, pendingSubscriptions } = clientDetails;
  const [showTaxonomy, setShowTaxonomy] = useState(false);
  const { name } = clientDetails;
console.log("CLients", clientDetails)
  return currentPath === "/clients" ? (
    <></>
  ) : (
    <Box
      display={currentPath === "/clients" ? "none" : "block"}
      background="gray.100"
    >
      <Flex pb="5" background="white">
        <Flex>
          <ArrowBackIcon
            color="blue"
            w={10}
            h="6"
            onClick={() => setCurrentPath("/clients")}
          />
          <Box>
            <Flex>
              <Box mr="5">
                <Heading size="md">{name}</Heading>
              </Box>
              <Select w="20" color="blue" variant="unstyled" size="xs">
                <option
                  selected={clientDetails.status === "active"}
                  value="active"
                >
                  Active
                </option>
                <option
                  selected={clientDetails.status === "deactivated"}
                  value="deactivate"
                >
                  Deactivated
                </option>
              </Select>
            </Flex>
            <Flex color="grey">
              <Text fontSize="xs" mr="2">
                Start Date
              </Text>
              <Text fontSize="xs" fontWeight="semibold">
                {clientDetails.startDate}
              </Text>
              <Text ml="10" mr="1" fontSize="xs">
                End Date
              </Text>
              <Text mr="2" fontSize="xs" fontWeight="semibold">
                {clientDetails.endDate}
              </Text>
              <Icon as={HiPencil} />
            </Flex>
          </Box>
        </Flex>
        <Spacer />
        {!showTaxonomy && (
          <Button colorScheme="blue" onClick={() => setShowTaxonomy(true)}>
            Add Subcategories
          </Button>
        )}
        {showTaxonomy && (
          <>
            <Button
              border="1px solid black"
              background="white"
              onClick={() => setShowTaxonomy(false)}
            >
              Cancel
            </Button>
            <AddSubscriptionModal />
          </>
        )}
      </Flex>
      <Flex mt="5" justifyContent="space-between">
        <Accordion
          ml="3"
          background="white"
          minW={showTaxonomy ? "65%" : "100%"}
          defaultIndex={[0]}
        >
          <SubscriptionItem heading="Active Subscriptions">
            <SubscriptionsAccordion subscriptions={activeSubscriptions} />
          </SubscriptionItem>
          <SubscriptionItem heading="Pending Subscriptions">
            <SubscriptionsAccordion showActionButtons={true} subscriptions={pendingSubscriptions} />
          </SubscriptionItem>
        </Accordion>

        <Box
          display={showTaxonomy ? "block" : "none"}
          w="32%"
          px="2"
          background="white"
          boxShadow="lg"
        >
          <TaxonomyAccordion />
        </Box>
      </Flex>
    </Box>
  );
};

function SubscriptionItem({ heading, children }) {
  return (
    <AccordionItem>
      <AccordionButton>
        <Box my="2" flex="1" textAlign="left">
          <h2>
            <Text fontSize="xl">{heading}</Text>
          </h2>
        </Box>
        <AccordionIcon />
      </AccordionButton>
      <AccordionPanel pb={4}>{children}</AccordionPanel>
    </AccordionItem>
  );
}
export default ActiveSubscriptions;
