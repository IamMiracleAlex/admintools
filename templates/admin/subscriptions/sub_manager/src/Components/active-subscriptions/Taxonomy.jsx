import {
  AccordionButton,
  AccordionItem,
  AccordionIcon,
  AccordionPanel,
  Accordion,
} from "@chakra-ui/accordion";
import { Checkbox, Heading, Input, useToast } from "@chakra-ui/react";
import { Box, Text, VStack } from "@chakra-ui/layout";
import React, { useEffect, useState, useContext } from "react";
import axios from "../axios";
import { AppContext } from "../../context/AppContext";
const SubcategoryList = ({
  subcategories,
  selectedSubcategories,
  setSelectedSubcategories,
}) => {
  const { selected } = useContext(AppContext);
  const [selectedItems, setSelectedItems] = selected;
  const subcategoryList = subcategories.map((subcategory, index) => {
    const { title, id } = subcategory;

    const handleChange = ({ target }) => {
      const { id, name } = target;
      const checked = selectedSubcategories[name] ? false : id;
      const newSelectedSubcategories = [...selectedSubcategories];
      newSelectedSubcategories[name] = checked;
      setSelectedSubcategories(newSelectedSubcategories);
      setSelectedItems({
        ...selectedItems,
        [subcategory.parent]: newSelectedSubcategories,
      });
    };
    return (
      <Checkbox
        isChecked={selectedSubcategories[index]}
        onChange={handleChange}
        key={id}
        id={id}
        name={index}
        colorScheme="blue"
      >
        <Text fontWeight="light">{title}</Text>
      </Checkbox>
    );
  });
  return <VStack align="start">{subcategoryList} </VStack>;
};

const Category = ({ category }) => {
  const { selected } = useContext(AppContext);
  const [selectedItems, setSelectedItems] = selected;
  const { title, id, children: subcategories } = category;
  const [selectedSubcategories, setSelectedSubcategories] = useState(
    new Array(subcategories.length).fill(false)
  );

  const allChecked = selectedSubcategories.every(Boolean);
  const isIndeterminate = selectedSubcategories.some(Boolean) && !allChecked;

  const handleChange = ({ target }) => {
    const checked = allChecked;
    const newSelected = subcategories.map((subcategory) => {
      return checked ? false : subcategory.id;
    });
    setSelectedSubcategories(newSelected);
    setSelectedItems({ ...selectedItems, [id]: newSelected });
  };

  return (
    <Accordion ml="2" borderColor="white" allowToggle allowMultiple>
      <AccordionItem>
        <AccordionButton border="none">
          <Box flex="1" textAlign="left">
            <Checkbox
              id={id}
              isChecked={allChecked}
              isIndeterminate={isIndeterminate}
              onChange={handleChange}
            >
              <Text fontWeight="light">{title}</Text>
            </Checkbox>
          </Box>
          <AccordionIcon />
        </AccordionButton>
        <AccordionPanel ml="5" pl="4" pb={4}>
          <SubcategoryList
            subcategories={subcategories}
            selectedSubcategories={selectedSubcategories}
            setSelectedSubcategories={setSelectedSubcategories}
          />
        </AccordionPanel>
      </AccordionItem>
    </Accordion>
  );
};

const CategoryList = (props) => {
  const categoryList = props.categories.map((category, index) => {
    return <Category {...props} key={category.id} category={category} />;
  });
  return <Box>{categoryList}</Box>;
};

const Department = (props) => {
  const { department } = props;
  const { title } = department;

  const handleChangeDepartment = () => {};

  return (
    <AccordionItem>
      <AccordionButton>
        <Box flex="1" textAlign="left">
          <Checkbox onChange={handleChangeDepartment} colorScheme="blue">
            <Text fontWeight="light">{title}</Text>
          </Checkbox>
        </Box>
        <AccordionIcon />
      </AccordionButton>
      <AccordionPanel>
        <CategoryList {...props} categories={department.children} />
      </AccordionPanel>
    </AccordionItem>
  );
};

const TaxonomyAccordion = ({ client_name, status }) => {
  const toast = useToast();
  const [taxonomy, setTaxonomy] = useState([]);
  useEffect(() => {
    axios
      .get("/classification/nodes/tree/")
      .then((res) => {
        setTaxonomy(res.data);
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

  const departments = taxonomy.map((department) => {
    return <Department key={department.id} department={department} />;
  });

  return (
    <Box px="2" boxShadow="lg">
      <VStack my="4">
        <Heading as="h4" size="sm">
          Add new category
        </Heading>
        <Text fontSize="sm" textAlign="center">
          Select the departments, categories or subcategories you would like to
          add
        </Text>
        <Input placeholder="search" type="text" />
      </VStack>
      <Accordion borderColor="white" allowToggle allowMultiple>
        {departments}
      </Accordion>
    </Box>
  );
};

export default TaxonomyAccordion;
