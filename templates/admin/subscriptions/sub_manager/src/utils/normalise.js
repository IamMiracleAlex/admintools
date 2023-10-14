/**
 *
 * @param {*} subscriptions (from our API)
 * @returns Object of the subcategories mapped to department and categories
 * the Returned object will look like:
 * {
 *  departmentTitle: {
 *      categoryTitle: { subcategory_id: {status, title}},
 *  },
 *  Grocery: {
 *      fruits: {
 *                1609: {status: "pending", subcategoryTitle: "apples"}
 *                1610: {status: "pending", subcategoryTitle: "oranges"}
 *            }
 *    }
 * }
 */
export const organizeSubscription = (subscriptions) => {
  const organizedSubscriptions = {};
  for (const subscription of subscriptions) {
    const { department, category, subcategory, subcategory_id, status } =
      subscription;

    if (!organizedSubscriptions[department])
      organizedSubscriptions[department] = {};

    if (!organizedSubscriptions[department][category])
      organizedSubscriptions[department][category] = [];

    organizedSubscriptions[department][category][subcategory_id] = {
      status,
      subcategory_id,
      subcategoryTitle: subcategory,
    };
  }
   
  return organizedSubscriptions;
};