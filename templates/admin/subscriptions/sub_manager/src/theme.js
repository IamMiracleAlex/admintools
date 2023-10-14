import { extendTheme } from "@chakra-ui/react";
// 2. Call `extendTheme` and pass your custom values
const theme = extendTheme({
  colors: {
    centricity: {
      link: "#064564",
      secondary: "#BEE2F2",
      highlight: "#FF6501",
      white: "#FFFFFF",
      background: "#FAFAFA",
      black: "#00000",
    },
  },
});

export default theme;
