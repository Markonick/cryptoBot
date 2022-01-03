import * as React from 'react';
import { GetSymbols } from '../../api/GetSymbols';
import { ISymbol } from "../../customTypes";
import CryptosTable from './CryptosTable';

export const Symbols: React.FC = () => {
  let symbols = []
  // symbols = GetSymbols() as ISymbol[];

  console.log('YOU CLICKED ON SYMBOLS LINK!!!')
  return (
    <div style={{marginTop: 100}}>
      <CryptosTable></CryptosTable>
    </div>
  );
};