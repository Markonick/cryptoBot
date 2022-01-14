import { useEffect, useState } from "react";
import { useRecoilValue } from "recoil";
import axios from "axios";
import { ISymbol } from "../customTypes";

export const GetSignals = () => {
  const [signals, setSignals] = useState<ISymbol[]>([]);
  const baseUrl = process.env.REACT_APP_BASE_URL;

  useEffect(() => {
    const fetchSignals = async () => {
      await axios.get<ISymbol[]>(`${baseUrl}/signals`).then(response => {
        setSignals(response?.data);
      });
    };
    fetchSignals();
  }, []);

  return (
    { signals }
  );
}
