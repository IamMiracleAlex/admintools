import React, { useContext, useState } from "react";
import { Button, Center, Spinner, Text, useToast } from "@chakra-ui/react";
import { useDisclosure } from "@chakra-ui/hooks";
import { CheckIcon, CloseIcon } from "@chakra-ui/icons";
import axios from "../axios";
import {
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  ModalContent,
  Modal,
} from "@chakra-ui/modal";
import { AppContext } from "../../context/AppContext";
import { organizeSubscription } from "../../utils/normalise";

function AddSubscriptionModal() {
  const toast = useToast();
  const { client, selected } = useContext(AppContext);
  const [clientDetails, setClientDetails] = client;
  const [selectedItems] = selected;
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [saving, setSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState("neutral");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSave = () => {
    const selectedSubcategories = [];
    for (const category in selectedItems) {
      const subcategories = selectedItems[category];
      for (const subcategory of subcategories) {
        if (subcategory)
          selectedSubcategories.push({
            subcategory_id: subcategory,
            status: "approved",
          });
      }
    }

    if (!selectedSubcategories.length) {
      setSaveStatus("error");
      setErrorMessage("Select A subcategory");
      return;
    }

    setSaving(true);

    axios
      .post(`/api/subscriptions/${clientDetails.id}/`, selectedSubcategories)
      .then((res) => {
        setSaving(false);
        setSaveStatus("success");

        axios
          .get(`api/subscriptions/${clientDetails.id}/?status=active`)
          .then((res) => {
            setClientDetails({
              ...clientDetails,
              subscriptions: organizeSubscription(res.data),
            });
            console.log(organizeSubscription(res.data));
          })
          .catch((err) => {
            toast({
              title: `Error Fetching Clients`,
              status: "error",
              isClosable: true,
              position: "top-right",
            });
          });
      })
      .catch((err) => {
        setSaving(false);
        setSaveStatus("error");
        setErrorMessage("Error saving subscription contact 😔");
      });
  };

  return (
    <>
      <Button
        ml="2"
        colorScheme="blue"
        onClick={() => {
          onOpen();
          handleSave();
        }}
      >
        Save Changes
      </Button>

      <Modal
        isOpen={isOpen}
        onClose={() => {
          onClose();
          setSaveStatus("neutral");
        }}
      >
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Adding Selected Subscriptions</ModalHeader>

          <ModalCloseButton />
          <ModalBody>
            {saving && (
              <Center>
                <Spinner
                  thickness="4px"
                  speed="0.65s"
                  emptyColor="gray.200"
                  color="blue.500"
                  size="xl"
                />
                Saving...
              </Center>
            )}

            {saveStatus === "success" && (
              <Center>
                <CheckIcon w={10} h={10} color="green" />
                Subscription Added
              </Center>
            )}

            {saveStatus === "error" && (
              <Center>
                <CloseIcon w={6} h={6} color="red" />
                <Text color="red">{errorMessage}</Text>
              </Center>
            )}
          </ModalBody>

          <ModalFooter>
            <Button
              size="xs"
              background="abudanza.secondary"
              color="black"
              colorScheme="blue"
              disabled={saving}
              mr={3}
              onClick={() => {
                onClose();
                setSaveStatus("neutral");
              }}
            >
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}

export default AddSubscriptionModal;
