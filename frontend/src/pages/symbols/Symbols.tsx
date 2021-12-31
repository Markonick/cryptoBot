import React, { useEffect } from "react";
import { useLocation } from 'react-router-dom';
import { styled } from '@mui/material/styles';
import { pageState } from '../../store/pageState';
import { useResetRecoilState } from "recoil";
import { createStyles, makeStyles } from '@mui/styles';

const useStyles = makeStyles({
  root: {
    marginTop: 60,
    display: 'flex',
    justifyContent: 'flex-start',
    flexDirection: 'row',
    backgroundColor: 'inherit',
    color: 'black',
    height: '100vh',
  }
});

export const Sites: React.FC = () => {
  const classes = useStyles();
  const resetPage = useResetRecoilState(pageState);

  useEffect(() => {
    resetPage()
  }, []);

  console.log('I AM RENDERING')

  return (
    <div style={{
      height: '100%',
      left: 0,
      position: 'fixed',
      top: 0,
      width: '100%',
    }}
    >
      <div className={classes.root}>
      </div>
    </div>);
};