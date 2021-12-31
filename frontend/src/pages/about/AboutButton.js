import React from "react";
import HelpIcon from '@material-ui/icons/Help';
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  root: {
    cursor: "pointer"
  },
  button: {
    marginRight: 20,
    marginLeft: 0,
    backgroundColor: "auto",
    color: "white",
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: "row",
    fontSize: "10px",
    opacity: "0.9",
    "&:hover": {
      color: "aqua",
      opacity: "1",
    }
  },
  modal: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: "white",
    flexDirection: "column",
  },
}));


function AboutButton(props) {
  const classes = useStyles();
  const aboutButton = (
    <div className={classes.button} onClick={props.func} >
      <HelpIcon fontSize='large' style={{ width: 20, height: 20, marginRight: 4 }} />
      ABOUT
    </div>
  );

  return (
    <div className={classes.root}>
      {aboutButton}
    </div >

  );
}

export default AboutButton;
