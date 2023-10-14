import React from "react";
import { BsArrowLeft } from "react-icons/bs";
import { Text, IconButton } from "@chakra-ui/react";

import ClientSkuMapper from "../ClientMapper/ClientSku";
import Mapper from "../Mapper";

export default function SkuWrapper() {
  const [isDetailView, setIsDetailView] = React.useState(false);
  const [client, setClient] = React.useState(false);

  const handleDetailView = (obj) => {
    setClient(obj);
    setIsDetailView(true);
  };

  return (
    <div className="container-fluid mb-5 pb-5 pt-3">
      <div className="all-url-header">
        <div className="d-flex justify-content-between">
          <div className="d-flex align-vertical">
            {isDetailView && (
              <IconButton
                icon={<BsArrowLeft size="2em" />}
                variant="ghost"
                onClick={() => setIsDetailView(false)}
              />
            )}
            <Text ml="4" fontSize="2xl" fontWeight="semibold">
              SKU Mapping
            </Text>
          </div>
        </div>
      </div>
      {isDetailView ? (
        <Mapper client={client} handleDetailView={handleDetailView} />
      ) : (
        <ClientSkuMapper handleDetailView={handleDetailView} />
      )}
    </div>
  );
}
