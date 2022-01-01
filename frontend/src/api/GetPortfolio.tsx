import { useEffect, useState } from "react";
import { useRecoilValue } from "recoil";
import axios from "axios";
import { ISymbol } from "../customTypes";

export const GetOrders = () => {
  const [symbols, setSymbols] = useState<ISymbol[]>([]);
  const baseUrl = process.env.REACT_APP_BASE_URL;

  useEffect(() => {
    const fetchSymbols = async () => {
      await axios.get<ISymbol[]>(`${baseUrl}/symbols`).then(response => {
        setSymbols(response?.data);
      });
    };
    fetchSymbols();
  }, []);

  return (
    { symbols }
  );
}
