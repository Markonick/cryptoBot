
import React from 'react';
import { makeStyles, useTheme } from "@mui/styles";
import { Theme } from '@mui/material';
import { styled } from '@mui/material/styles';
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { IAbout } from '../../customTypes';
import { Logo } from '../../components/Logo';

const StyledCard = styled(Card)({
  marginLeft: '25%',
  marginTop: '10%',
  display: "flex",
  flexWrap: "wrap",
  flexDirection: "row",
  justifyContent: "center",
  maxWidth: '50%',
  // backgroundColor: '#808080',
  boxShadow: "none",
});

const useStyles = makeStyles(({
  root: {
    marginTop: "20px",
    color: "black",
    boxShadow: 'none',
    // textDecoration: "none !important",
  },
  item: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "start-bottom",
    WebkitFontSmoothing: 'antialiased',
    marginBottom: 20,
  },
  title: {
    color: 'black',
    fontSize: 16,
    fontStyle: "normal",
    fontWeight: 400,
    fontFamily: "Helvetica",
  },
  text: {
    fontSize: 10,
    fontStyle: "normal",
    fontWeight: 100,
    fontFamily: "Helvetica",
    marginTop: 40,
    marginLeft: 20,
  },
  img: {
    height: "60px", width: "60px", marginRight: 20,
  },
  actions: {
    marginTop: "0.8%",
    display: "flex",
    justifyContent: "space-between"
  },
}));

interface Props {
  about: IAbout,
};

export const AboutCard: React.FC<Props> = (props: Props) => {
  const classes = useStyles();
  const theme = useTheme() as Theme;

  const aboutItems = [] as any;

  return (
    <div className={classes.root} 
      style={{backgroundColor: theme.palette.primary.about}}>
        <div className={classes.actions}>
          <div style={{
            textAlign: 'left', color: 'black'
          }}>
            {aboutItems}
          </div>
      </div>
    </div>
  )
};