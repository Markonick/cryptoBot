import React from "react";
import { makeStyles } from "@mui/styles";
import miaiqLogo from "../assets/images/miaiqLogo.png";


const useStyles = makeStyles(({
  root: {
    backgroundColor: "inherit",
    cursor: "pointer",
    marginRight: 20
  }
}));

type LogoProps = {
  width?: number
}
export const Logo: React.FC<LogoProps> = (props:LogoProps) => {
  const classes = useStyles();
  const { width = 100 } = props;

  const logo = (
    <div style={{ width: width }}>
      <img
        className={classes.root}
        width="80%"
        // src={miaiqLogo}
        src="https://www.kheironmed.com/wp-content/uploads/2021/08/MiaIQ-logo-white.png"
        alt="k-logo"
        // onClick={logoHandler}
      />
    </div>
  );
  return logo;
}