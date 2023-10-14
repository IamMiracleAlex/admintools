import { createContext, useState } from "react";

import React from "react";

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [client, setClient] = useState({});
  const [taxonomy, setTaxonomy] = useState([])
  const [selectedItems, setSelectedItems] = useState({})
  const [path, setPath] = useState('/clients')

  return (
    <AppContext.Provider
      value={{
        path: [path, setPath],
        selected: [selectedItems, setSelectedItems],
        client: [client, setClient],
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export default AppProvider;
