export const urlColors = [
  "#55B769",
  "#2A627C",
  "#F4B241",
  "#EE797C",
  "#FF0000",
  "#BA487F",
  "#BBA800",
];

export const formatMetricString = (str) => {
  return str.replace(/\_/g, " ").toUpperCase();
};

export const camelCaseStringToTitleCase = (str) => {
  return str.replace(/_/g, ' ').replace(/^./, s => s.toUpperCase())
}
