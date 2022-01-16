import { useEffect, useState } from "react";
import { useRecoilValue } from "recoil";
import axios from "axios";
import { IPortfolio } from "../customTypes";

export const GetPortfolio = () => {
  const [portfolio, setPortfolio] = useState<IPortfolio>();
  const baseUrl = process.env.REACT_APP_BASE_URL;

  useEffect(() => {
    const fetchPortfolio = async () => {
      await axios.get<IPortfolio>(`${baseUrl}/portfolio`).then(response => {
        setPortfolio(response?.data);
      });
    };
    fetchPortfolio();
  }, []);

  return (
    { portfolio }
  );
}
