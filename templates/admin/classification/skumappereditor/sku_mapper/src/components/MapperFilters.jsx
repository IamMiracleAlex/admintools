import React from 'react';
import Search from './Search'
import { Flex, Box, Select, HStack } from "@chakra-ui/react"

const MapperFilters = ({ handleSearch }) => {

    return (
        <Flex direction="row-reverse">
            <Box p="4" align="right" style={{float: "right"}}>
                <HStack spacing="10px">
                    <Select placeholder="Department">
                        <option value="option1">Option 1</option>
                        <option value="option2">Option 2</option>
                        <option value="option3">Option 3</option>
                    </Select>
                    <Select placeholder="Category">
                        <option value="option1">Option 1</option>
                        <option value="option2">Option 2</option>
                        <option value="option3">Option 3</option>
                    </Select>
                    <Select placeholder="Sub-category">
                        <option value="option1">Option 1</option>
                        <option value="option2">Option 2</option>
                        <option value="option3">Option 3</option>
                    </Select>
                    <Select placeholder="Subset">
                        <option value="option1">Option 1</option>
                        <option value="option2">Option 2</option>
                        <option value="option3">Option 3</option>
                    </Select>
                    <Search placeholder="Search" onChange={handleSearch} />
                </HStack>
            </Box>
        </Flex>
    );
}

export default MapperFilters;