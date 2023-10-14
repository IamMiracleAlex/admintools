export const getErrorMessage = (errObj) => {
  const errResponse = errObj.response;
  if (errObj.message) return errObj.message;
  const errorMessage = errResponse?.data?.detail
    ? errObj.detail
    : "Something went Wrong, Please try again";
  return errorMessage;
};

export const isClientActive = (client) => {
  let unique_client = client[0];
  if (unique_client) {
    return unique_client.user.is_active ? "Active" : "Inactive";
  }
  return "N/A";
};

const formatDate = (date) => {
  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  if (!date) return "N/A";

  let d = new Date(date);

  let year = d.getFullYear();
  let month = d.getMonth() + 1;
  let day = d.getDate();
  let hours = d.getHours();
  let minutes = d.getMinutes();

  let ampm = hours >= 12 ? "pm" : "am";

  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? "0" + minutes : minutes;

  d = `${months[month]} ${day}, ${year} - ${hours}:${minutes}${ampm}`;

  return d;
};

export { formatDate };
