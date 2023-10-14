import React from "react";

const useSortableClients = (clients, config = null) => {
  const [sortConfig, setSortConfig] = React.useState(config);

  const sortedClients = React.useMemo(() => {
    let sortableClients = [...clients];
    if (sortConfig !== null) {
      sortableClients.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === "asc" ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === "asc" ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableClients;
  }, [clients, sortConfig]);

  const sortBy = (key) => {
    let direction = "asc";
    if (
      sortConfig &&
      sortConfig.key === key &&
      sortConfig.direction === "asc"
    ) {
      direction = "desc";
    }
    setSortConfig({ key, direction });
  };

  return { sortedClients, sortBy, sortConfig };
};

export default useSortableClients;
