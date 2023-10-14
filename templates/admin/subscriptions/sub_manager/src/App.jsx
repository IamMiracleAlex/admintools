import React from "react";
import { ChakraProvider } from "@chakra-ui/react";

import "./App.css";
import Nav from "./Components/common/Nav";
import ClientsTable from "./Components/client-subscription/ClientsTable";
import Subscriptions from "./Components/active-subscriptions/SubscriptionsPage";
import AppProvider from "./context/AppContext";

function App() {

  return (
    <ChakraProvider>
      <AppProvider>
        <Nav>
          <ClientsTable />
          <Subscriptions />
        </Nav>
      </AppProvider>
    </ChakraProvider>
  );
}

export default App;
