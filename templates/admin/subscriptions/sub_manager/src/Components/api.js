import { organizeSubscription } from "../utils/normalise";
import axios from "./axios";


export const getPendingSubs = ({toast, client, setSelectedClient}) =>
  axios
    .get(`api/subscriptions/${client.id}/?status=inactive`)
    .then((res) => {
      setSelectedClient({
        ...client,
        pendingSubscriptions: organizeSubscription(res.data),
      });
    })
    .catch((err) => {
      toast({
        title: `Error Fetching Clients`,
        status: "error",
        isClosable: true,
        position: "top-right",
      });
    });

    export const getActiveSubs = ({ toast, client, setSelectedClient }) =>
      axios
        .get(`api/subscriptions/${client.id}/?status=approved`)
        .then((res) => {
          setSelectedClient({
            ...client,
            activeSubscriptions: organizeSubscription(res.data),
          });
        })
        .catch((err) => {
          toast({
            title: `Error Fetching Clients`,
            status: "error",
            isClosable: true,
            position: "top-right",
          });
        });