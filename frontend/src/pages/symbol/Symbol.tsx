import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { createStyles, makeStyles } from '@mui/styles';
import { ISymbol } from "../../customTypes";


export const Study: React.FC<ISymbol> = () => {
  const location = useLocation<ISymbol>();

  const symbol = location.state;

  return (
      <div> {symbol}</div>
  )
};
