
import React from 'react';
import { makeStyles, useTheme } from "@mui/styles";
import { Theme } from '@mui/material';
import { styled } from '@mui/material/styles';
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import ce from '../../assets/images/ce.svg';
import consult from '../../assets/images/instruction.svg';
import manufactureDate from '../../assets/images/date.svg';
import manufacturer from '../../assets/images/manufacturer.svg';
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

const StyledCardContent = styled(CardContent)({
  width: '80%',
  display: "flex",
  flexWrap: "wrap",
  flexDirection: "row",
  justifyContent: "center",
  // backgroundColor: 'red',
});

const StyledTypography = styled(Typography)({
  display: "flex",
  flexWrap: "wrap",
  fontWeight: 100,
  fontFamily: "Helvetica",
  color: 'black',
  fontSize: 14,
  width: '100%',
});
const useStyles = makeStyles(({
  root: {
    marginTop: "20px",
    // color: "black",
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

  const versionNumber = props.about.miaIqVersion || 'Version 1.1.0';
  const miaIqVersionItem = (
    <div className={classes.item} >
      <Typography className={classes.img} style={{marginRight: 20, height: 30,}}><Logo width={80}/></Typography>
      <StyledTypography className={classes.text}>{versionNumber}</StyledTypography>
    </div>);

  const consultText = {
    EU: "This is not a  medical device. Not intended to mitigate, treat or diagnose a disease. Consult instruction for use",
    US: "Consult instruction for use",
  };

  const consultInfo = (
    <div className={classes.item}>
      <img src={consult} className={classes.img} alt="consult" />
      <StyledTypography className={classes.text}>{consultText.EU}</StyledTypography >
    </div>);

  const ceMarkNumber = props.about.ceMarkNumber || '197';
  const ceMark = (
    <div className={classes.item}>
      <img src={ce} className={classes.img} alt="cemark" />
      <StyledTypography className={classes.text}>{ceMarkNumber}</StyledTypography >
    </div>
  );

  const manufacturerText = (
    <div>
      <div>Kheiron Medical Technologies Ltd</div>
      <div>Stylus Building, 116 Old Street</div>
      <div>London EC1V 9BG</div>
      <div>United Kingdom</div>
    </div>
  );

  const manufacturerItem = (
    <div className={classes.item}>
      <img src={manufacturer} className={classes.img} alt="manufacturer" />
      <StyledTypography className={classes.text} style={{ marginTop: 0 }}>{manufacturerText}</StyledTypography >
    </div>);

  const manufactureDateText = '22 Mar 2021';
  const manufactureDateItem = (
    <div className={classes.item}>
      <img src={manufactureDate} className={classes.img} alt="manufactureDate" />
      <StyledTypography className={classes.text}>{manufactureDateText}</StyledTypography >
    </div>);

  const aboutItems = [
    miaIqVersionItem,
    consultInfo,
    ceMark,
    manufacturerItem,
    manufactureDateItem,
  ]

  return (
    <StyledCard className={classes.root} 
      style={{backgroundColor: theme.palette.primary.about}}>
      <StyledCardContent>
        <div className={classes.actions}>
          <div style={{
            textAlign: 'left',
          }}>
            {aboutItems}
          </div>
        </div>
      </StyledCardContent>
    </StyledCard >
  )
};