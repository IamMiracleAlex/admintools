import React, { useState, useEffect } from "react";
import {
  Flex,
  IconButton,
  Text,
  NumberInput,
  NumberInputField,
} from "@chakra-ui/react";
import { FaAngleLeft, FaAngleRight } from "react-icons/fa";

function Paginations({ totalPages, paginate, current, size="sm", ...rest }) {
  const pageMin = 1;

  const [currentPage, setCurrentPage] = useState(pageMin);

  useEffect(() => {
    setCurrentPage(current);
  }, [current]);

  const gotoPage = (pageNumber) => {
    let pageValue = parsePageValue(pageNumber);

    paginate(pageValue);
    setCurrentPage(pageValue);
  };

  const parsePageValue = (value) => {
    let p;
    if (value > totalPages) return;

    if (typeof value == "string" && !value.trim()) {
      p = value;
    } else {
      p = Number(value);
      if (p < pageMin) return;
    }
    return p;
  };

  return (
    <Flex justifyContent="flex-end" m={4} alignItems="center">
      <Text>displaying page</Text>
      <Flex>
        <IconButton
        size={size}
          variant="outline"
          colorScheme="blue"
          aria-label="Next Page"
          borderRadius="3"
          onClick={() => gotoPage(currentPage - pageMin)}
          isDisabled={currentPage <= pageMin}
          icon={<FaAngleLeft h={3} w={3} />}
          ml={4}
        />
      </Flex>

      <Flex alignItems="center">
        <NumberInput
          mr={2}
          size={size}
          min={pageMin}
          max={totalPages}
          maxW={16}
          defaultValue={pageMin}
          value={currentPage}
          onChange={(value) => {
            gotoPage(value);
          }}
        >
          <NumberInputField size={size} borderRadius="3" />
        </NumberInput>
      </Flex>

      <Text fontSize="sm" ml="1"> of </Text>
      <Text fontSize="sm" ml="2" color="blue">
        {totalPages}
      </Text>

      <Flex>
        <IconButton
        size={size}
          variant="outline"
          colorScheme="blue"
          aria-label="Next Page"
          borderRadius="3"
          onClick={() => gotoPage(current + pageMin)}
          isDisabled={current >= totalPages}
          icon={<FaAngleRight h={3} w={3} />}
          ml={4}
        />
      </Flex>
    </Flex>
  );
}

export default Paginations;
