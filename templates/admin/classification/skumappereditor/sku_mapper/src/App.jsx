import React from 'react';
import "./App.css";
import { ChakraProvider } from "@chakra-ui/react";
import { QueryParamProvider } from "use-query-params";
import SkuWrapper from "./components/SkuWrapper";
import customTheme from "./CustomTheme";

function App() {
  return (
    <>
      <ChakraProvider theme={customTheme}>
        <QueryParamProvider>
          <SkuWrapper />
        </QueryParamProvider>
      </ChakraProvider>
    </>
  );
}

export default App;
