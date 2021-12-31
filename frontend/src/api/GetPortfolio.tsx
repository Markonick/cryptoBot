import { useEffect, useState } from "react";
import { useRecoilValue } from "recoil";
import axios from "axios";
import { tokenState } from '../store/tokenState';
import { ISummary } from "../customTypes";

const initialSummary = {
  "site":1,
  "total_studies":0,
  "view_summaries":{
    "CC":{
      "compression":{"overall":{"too_little":0,"too_much":0,"optimal":0,"minimum":0,"maximum":0,"average":0},"groups":{"small":{"too_little":0,"too_much":0,"optimal":2,"minimum":0,"maximum":0,"average":0},"medium":{"too_little":0,"too_much":0,"optimal":0,"minimum":0,"maximum":0,"average":0},"large":{"too_little":0,"too_much":0,"optimal":0,"minimum":0,"maximum":0,"average":0}}},
      "positioning":{
        "total":0,
        "classification":{
          "adequate":{"percentage":0,"count":0},
          "indeterminate":{"percentage":0,"count":0},
          "inadequate":{"percentage":0,"count":0}},
          "criteria":{"No Pectoral Muscle":{"percentage":0,"count":0},"Nipple Not In Profile":{"percentage":0,"count":0},"Nipple Not Centered":{"percentage":0,"count":0},"Insufficient Medial Part":{"percentage":0,"count":0},"Insufficient Spread Out":{"percentage":0,"count":0},"Blur":{"percentage":0,"count":0},"Insufficient Lateral Part":{"percentage":0,"count":0},"Less Imaged Than Previous":{"percentage":0,"count":0},"Asymmetry":{"percentage":0,"count":0},"Lateral Folds":{"percentage":0,"count":0},"Medial Folds":{"percentage":0,"count":0},"Central Folds":{"percentage":0,"count":0}}
        }
    },
    "MLO":{
      "compression":{"overall":{"too_little":0,"too_much":0,"optimal":2,"minimum":140,"maximum":150,"average":0},"groups":{"small":{"too_little":0,"too_much":0,"optimal":2,"minimum":140,"maximum":150,"average":0},"medium":{"too_little":0,"too_much":0,"optimal":0,"minimum":0,"maximum":0,"average":0},"large":{"too_little":0,"too_much":0,"optimal":0,"minimum":0,"maximum":0,"average":0}}},
      "positioning":{
        "total":2,
        "classification":{
          "adequate":{"percentage":0,"count":0},
          "indeterminate":{"percentage":0,"count":0},
          "inadequate":{"percentage":0,"count":0}},
          "criteria":{"No Inframammary Angle":{"percentage":0,"count":0},"Bucky Not Set In Center":{"percentage":0,"count":0},"Pectoral Muscle Insufficient Wide":{"percentage":0,"count":0},"Blur":{"percentage":0,"count":0},"Nipple Not In Profile":{"percentage":0,"count":0},"Pectoral Muscle Not At Nipple Level":{"percentage":0,"count":0},"Insufficient Spread Out":{"percentage":0,"count":0},"Less Imaged Than Previous":{"percentage":0,"count":0},"Asymmetry":{"percentage":0,"count":0},"Folds Inframammary":{"percentage":0,"count":0},"Folds Pectoral":{"percentage":0,"count":0}}}
        }
    }
}
export const GetSummary = (siteId:number) => {
  const [summary, setSummary] = useState<ISummary>(initialSummary);
  const baseUrl = process.env.REACT_APP_BASE_URL;
  const token = useRecoilValue(tokenState);
  const config = {
    headers: { "Authorization": `Bearer ${token}`}
  };

  useEffect(() => {
    const fetchSummary = () => {
      axios.get<ISummary>(`${baseUrl}/summary/${siteId}`, config)
      .then(response => {
        setSummary(response?.data);
      })
      .catch(error => {
        console.log(error)
      });
    };
    fetchSummary();
  }, []);
  
  return (
    {summary}
  );
}
    