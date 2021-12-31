import React from "react";
import { makeStyles } from "@mui/styles";
import { useLocation } from 'react-router-dom';
import { AccountInfo } from "@azure/msal-common";


const useStyles = makeStyles(({
  root: {
    backgroundColor: "inherit",
    cursor: "pointer",
    marginRight: 20
  }
}));

export const Profile: React.FC = () => {
  const classes = useStyles();
  const location = useLocation();
  const account = location.state as any;
  console.log(account)
  const idTokenClaims = account.account.idTokenClaims;
  console.log(idTokenClaims)
	const firstName = account.account.idTokenClaims.given_name;
	const surname = account.account.idTokenClaims.family_name;
	const username = account.account.name;
  const items = [username, firstName, surname]
  return (<>{Object.keys(idTokenClaims).map((key, i) =>  (<p>{key}: {idTokenClaims[key]}</p>))}</>);
  // return (<>{items}</>);
  // return (<>{'abc'}</>);
}