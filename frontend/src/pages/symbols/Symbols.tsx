import * as React from 'react';
import { GetSymbols } from '../../api/GetSymbols';
import { ISymbol } from "../../customTypes";

export const Symbols: React.FC = () => {
  let symbols = []
  symbols = GetSymbols() as ISymbol[];

  console.log('YOU CLICKED ON SYMBOLS LINK!!!')
  return (
    <>
      {symbols}
    </>
  );
};