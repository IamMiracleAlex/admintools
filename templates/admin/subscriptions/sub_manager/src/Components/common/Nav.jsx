import React from 'react'
import Icon from "@chakra-ui/icon";
import { Input } from "@chakra-ui/input";
import { Box, Divider, HStack, Spacer, Text } from "@chakra-ui/layout"
import { IoIosHelpCircleOutline } from "react-icons/io";

const Nav = ({children})=>{
    return (
      <Box mx="5" >
        <Box mb="7">
          <HStack>
            <Text>Subscription Management</Text>
            <Spacer/>
           
            <Input w="50%" placeholder="Search" /> <Icon as={IoIosHelpCircleOutline}/>
          </HStack>
          <Divider mt="2"/>
        </Box>
        {children}
      </Box>
    );
}

export default Nav