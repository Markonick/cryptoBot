import React from "react";
import { makeStyles } from "@mui/styles";
import miaiqLogo from "../assets/images/doge3.png";


const useStyles = makeStyles(({
  root: {
    backgroundColor: "inherit",
    cursor: "pointer",
    margin: 20
  }
}));

type LogoProps = {
  width?: number
}
export const Logo: React.FC<LogoProps> = (props:LogoProps) => {
  const classes = useStyles();
  const { width = 70 } = props;

  const logo = (
    <div style={{ width: width }}>
      <img
        className={classes.root}
        width="100%"
        src={miaiqLogo}
        // src="https://www.kheironmed.com/wp-content/uploads/2021/08/MiaIQ-logo-white.png"
        alt="k-logo"
        // onClick={logoHandler}
      />
    </div>
  );
  return logo;
}