import {
  AccordionButton,
  AccordionItem,
  AccordionIcon,
  AccordionPanel,
  Accordion,
} from "@chakra-ui/accordion";
import {
  Box,
  Text,
  LinkBox,
  LinkOverlay,
  Wrap,
  HStack,
  Divider,
} from "@chakra-ui/layout";
import { ButtonGroup, Spacer, Button, useToast } from "@chakra-ui/react";
import React, { useState } from "react";
import { useContext } from "react";
import { AppContext } from "../../context/AppContext";
import { getActiveSubs, getPendingSubs } from "../api";
import axios from "../axios";

const SubcategoryList = ({ subcategories }) => {
  const subcategoryList = [];
  for (const subcategory in subcategories) {
    subcategoryList.push(
      <Box
        key={subcategory}
        py="1"
        px="2"
        background="white"
        boxShadow="md"
        borderRadius="sm"
      >
        <Text fontSize="md" textTransform="lowercase">
          {subcategories[subcategory].subcategoryTitle}
        </Text>
      </Box>
    );
  }

  return <Wrap>{subcategoryList}</Wrap>;
};

const Category = ({ category, title, showActionButtons }) => {
  const toast = useToast();
  const { client } = useContext(AppContext);
  const [selectedClient, setSelectedClient] = client;
  const [showSubcategory, setShowSubcategories] = useState(false);
  const [selectedSubcategories, setSelectedSubcategories] = useState({});
  const [updating, setUpdating] = useState(false);

  const updateSubscription = (update) =>
    axios
      .patch(`api/subscriptions/${selectedClient.id}/bulk_update/`, update)
      .then((res) => {
        setUpdating(false);
        toast({
          title: `Successfully Updated Subscriptions`,
          status: "success",
          isClosable: true,
          position: "top-right",
        });
        getActiveSubs({ toast, client: selectedClient, setSelectedClient });
        getPendingSubs({ toast, client: selectedClient, setSelectedClient });
      })
      .catch((err) => {
        setUpdating(false);
      });

  const handleApproval = (status) => {
    const update = [];
    for (const subcategory in category) {
      update.push({ subcategory_id: subcategory, status });
    }
    updateSubscription(update);
  };

  return (
    <>
      <LinkBox pb="4" onClick={() => setShowSubcategories(!showSubcategory)}>
        <HStack>
          <LinkOverlay href="#">
            <Text color="black" fontSize="md">
              {title}
            </Text>
          </LinkOverlay>
          <Spacer />
          {showActionButtons && (
            <ButtonGroup size="xs" variant="solid" spacing="4">
              <Button
                colorScheme="green"
                onClick={() => handleApproval("approved")}
              >
                Approve All
              </Button>
              <Button
                colorScheme="red"
                onClick={() => handleApproval("rejected")}
              >
                Reject All
              </Button>
            </ButtonGroup>
          )}
        </HStack>
      </LinkBox>
      <Box pb="5" display={showSubcategory ? "block" : "none"}>
        <SubcategoryList subcategories={category} />
      </Box>
    </>
  );
};

const CategoryList = ({ categories, ...props }) => {
  const categoryList = [];

  for (const category in categories) {
    categoryList.push(
      <Category
        key={category}
        title={category}
        category={categories[category]}
        {...props}
      />
    );
  }
  return <Box>{categoryList}</Box>;
};

const Department = ({ department, title, ...props }) => {
  return (
    <AccordionItem key={department}>
      <AccordionButton
        _expanded={{ bg: "#487BC2", color: "white" }}
        _hover={{ bg: "#487BC2", color: "white" }}
      >
        <Box my="2" flex="1" textAlign="left">
          <Text as="h2" fontSize="lg">
            {title}
          </Text>
        </Box>
        <AccordionIcon />
      </AccordionButton>
      <AccordionPanel pb={4} background="#FAFBFC">
        <CategoryList  categories={department} {...props}/>
      </AccordionPanel>
    </AccordionItem>
  );
};

const SubscriptionsAccordion = ({ subscriptions , showActionButtons}) => {
  const departments = [];

  for (const department in subscriptions) {
    departments.push(
      <Department
        title={department}
        key={department}
        department={subscriptions[department]}
        showActionButtons={showActionButtons}
      />
    );
  }

  return <Accordion allowToggle>{departments}</Accordion>;
};

export default SubscriptionsAccordion;
