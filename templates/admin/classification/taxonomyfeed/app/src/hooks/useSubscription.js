import { useEffect, useState } from 'react';

/**
 * Subscribe to a local stream. You can also bind a remote subscription
 * to the stream you are subscribing to.
 */
export const useSubscription = (localStream) => {
    const [subscriptionValue, setSubscriptionValue] = useState();

    /**
     * Subscribe to the subject and populate the state value with the stream
     * value that changes over time.
     */
    useEffect(() => {
        const subscription = localStream.subscribe((data) => setSubscriptionValue(data));

        // Make sure that the subscription is unsubscribed on unmount.
        return () => subscription.unsubscribe();
    }, [localStream]);

    // Return the subscription value.
    return subscriptionValue;
};
