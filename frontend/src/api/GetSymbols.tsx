import { useEffect, useState } from "react";
import { useRecoilValue } from "recoil";
import axios from "axios";
import { ISite } from "../customTypes";
import { tokenState } from '../store/tokenState';

export const GetSites = () => {
  const [sites, setSites] = useState<ISite[]>([]);
  const baseUrl = process.env.REACT_APP_BASE_URL;
  const token = useRecoilValue(tokenState);
  const config = {
    headers: { "Authorization": `Bearer ${token}`}
  };

  useEffect(() => {
    const fetchSites = async () => {
      await axios.get<ISite[]>(`${baseUrl}/sites/1`, config).then(response => {
        setSites(response?.data);
      });
    };
    fetchSites();
  }, []);
  
  return (
    {sites}
  );
}
    