import { createTheme } from "@mui/material/styles";


  const darkTheme = createTheme({
	status: {
	  danger: '#e53e3e',
	},
	palette: {
		mode: 'dark',
	  primary: {
		main: '#000000',
		header: '#0d0d0d',
		sidepanel: '#090909',
		footer: '#0d0d0d', 
		text: '#e6e6e6',
		paper: '#1a1a1a', 
		rowColorHover: '#262626',
		rowBackColorHover: '#1a1a1a',
		about: '#7FFFD4',
		siteCardBckgColor: "#1a1a1a",
		siteCardBckgColorHover: "#0d0d0d",
		siteCardTitleColor: "white",
		siteCardTitleColorHover: "black",
		siteCardDateColor: "aqua",
		siteCardDateColorHover: "magenta",
		adequate: "#98ffeb",
		indeterminate: "yellow",
	  },
	},
  });

  const lightTheme = createTheme({
	status: {
	  danger: '#e53e3e',
	},
	palette: {
		mode: 'light',
	  primary: {
		main: '#FFFFFF',
		header: '#e6e6e6',
		sidepanel: '#f2f2f2',
		footer: '#e6e6e6',
		text: '#000000',
		paper: '#f2f2f2',
		rowColorHover: '#cccccc',
		rowBackColorHover: '#DCFFFF',
		about: 'Gainsboro',
		siteCardBckgColor: "#DCFFFF",
		siteCardTitleColor: "black",
		siteCardTitleColorHover: "black",
		siteCardDateColor: "magenta",
		siteCardDateColorHover: "magenta",
		adequate: "#00C1D4",
		indeterminate: "#F9D00F",
		// siteCardBckgColor: "#A9A9A9",
		// siteCardBckgColorHover: "#0d0d0d",
		// siteCardTitleColor: "white",
		// siteCardTitleColorHover: "black",
		// siteCardDateColor: "cyan",
		// siteCardDateColorHover: "magenta",
	},
	},
  });
declare module '@mui/material/styles' {
	interface Theme {
	  status: {
		danger: React.CSSProperties['color'];
	  };
	}
  
	interface Palette {
	  secondary: Palette['secondary'];

	}
	interface PaletteOptions {
		// secondary: PaletteOptions['secondary'];
	}
  
	interface PaletteColor {
	  dark1?: string;
	  dark2?: string;
	  dark3?: string;
	  header?: string;
	  sidepanel?: string;
	  footer?: string;
	  text?: string;
	  paper?: string;
	  rowColorHover?: string;
	  rowBackColorHover?: string;
	  about?: string;
	  siteCardBckgColor?: string;
	  siteCardBckgColorHover?: string;
	  siteCardTitleColor?: string;
	  siteCardTitleColorHover?: string;
	  siteCardDateColor?: string;
	  siteCardDateColorHover?: string;
	  adequate?: string;
	  indeterminate?: string;
	}

	interface SimplePaletteColorOptions {
	  dark1?: string;
	  dark2?: string;
	  dark3?: string;
	  header?: string;
	  sidepanel?: string;
	  footer?: string;
	  text?: string;
	  paper?: string;
	  rowColorHover?: string;
	  rowBackColorHover?: string;
	  about?: string;
	  siteCardBckgColor?: string;
	  siteCardBckgColorHover?: string;
	  siteCardTitleColor?: string;
	  siteCardTitleColorHover?: string;
	  siteCardDateColor?: string;
	  siteCardDateColorHover?: string;
	  adequate?: string;
	  indeterminate?: string;
	}

	interface ThemeOptions {
	  status: {
		danger: React.CSSProperties['color'];
	  };
	}
  }

export { darkTheme, lightTheme }