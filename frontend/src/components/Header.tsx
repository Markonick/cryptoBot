import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useRecoilValue, useSetRecoilState } from "recoil";
import { makeStyles, useTheme, createStyles } from "@mui/styles";
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import HelpIcon from '@mui/icons-material/Help';
import CssBaseline from '@mui/material/CssBaseline';
import { ROUTES_CONFIG } from '../routes';
import { Logo } from "./Logo";
import { siteState } from '../store/siteState';
import { tokenState } from '../store/tokenState';
import { summaryState } from '../store/summaryState';
import { AuthenticatedTemplate, useMsal, useAccount} from "@azure/msal-react";
import { AccountMenu } from './AccountMenu';
import { Theme } from '@mui/material';
import { apiRequest } from '../pages/auth/authConfig';

const colorArray = {
  "dark": ["crimson", "pink", "springgreen", "orange",],
  "light": ["crimson", "black", "#0000ff", "green",],
};

const getRandomColor = (mode: string) => colorArray[mode  as keyof typeof colorArray][Math.floor(Math.random() * colorArray["dark"].length)];

const useStyles =  makeStyles((theme: Theme) => 
  createStyles({
  root: {
    // marginBottom: "10%",
  },
  navbar: {
    display: "flex",
    flexwrap: "wrap",
    flexDirection: "row",
    justifyContent: "center",
    marginLeft: "0%",
  },
  logo: {
    // marginLeft: 'auto',
    marginRight: 'auto',
    paddingLeft: 0,
    fontStyle: "normal",
    fontWeight: 600,
    WebkitFontSmoothing: 'antialiased',
    color: "black",
    textDecoration: "none! important",
  },
  link: {
    marginLeft: 30,
    fontSize: 11,
    fontStyle: "normal",
    fontWeight: 200,
    fontFamily: "Helvetica",
    textTransform: 'uppercase',
    letterSpacing: '1px',
    lineHeight: '1.3em',
    WebkitFontSmoothing: 'antialiased',
    color: getRandomColor(theme.palette.mode),
    filter: 'brightness(140%)',
    display: "flex",
    flexDirection: "row",
    textDecoration: "none",
    transition: '1s',
    "&:hover": {
      color: getRandomColor(theme.palette.mode),
      transition: "0.7s",
      textDecoration: "underline deeppink",
    },
    "&:focus": {
      color: getRandomColor(theme.palette.mode),
      transition: "0.7s",
      textDecoration: "underline deeppink",
    }
  },
  disabled: {
    pointerEvents: 'none',
  }
}));

export const Header: React.FC = (props) => {
  const classes = useStyles();
  const theme = useTheme() as Theme;
  const site = useRecoilValue(siteState);
  const summary = useRecoilValue(summaryState);
  const setToken = useSetRecoilState<string>(tokenState);

	const { accounts, instance } = useMsal();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);
  const account = useAccount(accounts[0] || {});

  useEffect(() => {
    if (account) {
      instance.acquireTokenSilent({
          scopes: apiRequest.scopes,
          account: account
      }).then((response) => {
          if(response) {
            setToken(response.accessToken)
          }
      });
    }
  }, [account, instance, setToken]);

  const isSiteSelected = Object.keys(site).length > 0;
  const isSummarySelected = Object.keys(summary).length > 0;

  const conditionalSummaryLink = isSiteSelected 
    ? <Link to={{pathname: ROUTES_CONFIG.SUMMARY, state: site}} className={classes.link}>SUMMARY</Link>
    : "";

  const conditionalStudiesLink = isSummarySelected
    ? <Link to={{pathname: ROUTES_CONFIG.ALL_STUDIES_LIST, state: {site_id: site.id}}} className={classes.link}>ALL STUDIES</Link>
    : "";

  return (
    <React.Fragment >
      <CssBaseline />
      {/* <HideOnScroll {...props}> */}
        <AppBar className={classes.root} elevation={0} style={{
          backgroundColor: theme.palette.primary.header, 
          }}>
          <Toolbar className={classes.navbar}>
            <AuthenticatedTemplate>
              <Link to={ROUTES_CONFIG.ROOT} className={classes.logo}><Logo/></Link>
              <Link to={ROUTES_CONFIG.ROOT} className={classes.link}>SITES</Link>
              {conditionalSummaryLink}
              {conditionalStudiesLink}
              <Link to={ROUTES_CONFIG.ABOUT} className={classes.link}><HelpIcon fontSize='small' style={{ display: "flex", marginRight: 5, marginTop: -5}} />ABOUT</Link>    
              <AccountMenu account={accounts[0]} color={getRandomColor(theme.palette.mode)}/>
            </AuthenticatedTemplate>
          </Toolbar>
        </AppBar>
      {/* </HideOnScroll> */}
      <Toolbar/>
    </React.Fragment>
  );
}