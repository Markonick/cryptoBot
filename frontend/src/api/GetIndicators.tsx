import { useEffect, useState } from "react";
import { useRecoilValue } from "recoil";
import axios from "axios";
import { tokenState } from '../store/tokenState';
import { ISearchFilter, IStudyPair } from "../customTypes";

import image0 from '../assets/images/1.2.826.0.1.10184103.9.3.5348.png';
import image1 from '../assets/images/1.2.826.0.1.10184103.9.3.5349.png';
import image2 from '../assets/images/1.2.826.0.1.10184103.9.3.5350.png';
import image3 from '../assets/images/1.2.826.0.1.10184103.9.3.5351.png';

const urlBlob0 = {
  url: "image0"
};

const urlBlob1 = {
  url: "image0"
};

const urlBlob2 = {
  url: "image0"
};

const urlBlob3 = {
  url: "image0"
};

const testCriteriaAssessment = {
  id: 1,
  adequate: "Adequate",
  name: "test_criteria",
};
const testImageAssessment = {
  adequate: "Adequate",
  criteria: [testCriteriaAssessment, testCriteriaAssessment, testCriteriaAssessment, testCriteriaAssessment],
};

const testImage1 = {
  id: 0,
  uid: '6.6.6.6',
  laterality: 'L',
  view: 'CC',
  compression: 139,
  preview_png: urlBlob0,
  original_png: urlBlob0,
  segmentation_svg: urlBlob0,
  assessment: testImageAssessment,
};

const testImage2 = {
  id: 1,
  uid: '6.6.6.7',
  laterality: 'R',
  view: 'CC',
  compression: 140,
  preview_png: urlBlob1,
  original_png: urlBlob1,
  segmentation_svg: urlBlob1,
  assessment: testImageAssessment,
};
const testImage3 = {
  id: 2,
  uid: '6.6.6.8',
  laterality: 'L',
  view: 'MLO',
  compression: 141,
  preview_png: urlBlob2,
  original_png: urlBlob2,
  segmentation_svg: urlBlob2,
  assessment: testImageAssessment,
};
const testImage4 = {
  id: 3,
  uid: '6.6.6.9',
  laterality: 'R',
  view: 'MLO',
  compression: 142,
  preview_png: urlBlob3,
  original_png: urlBlob3,
  segmentation_svg: urlBlob3,
  assessment: testImageAssessment,
};

const testStudy = {
  id : 0,
  uid : '3.3.3.3',
  images : {"CC-L": testImage1, "CC-R": testImage2, "MLO-L": testImage3, "MLO-R": testImage4},
  revision : 0,
};

const testStudyPair = {
  latest: testStudy,
}

const initialStudyPairsValue = [
  testStudyPair, testStudyPair, testStudyPair, testStudyPair, testStudyPair,
  testStudyPair, testStudyPair, testStudyPair, testStudyPair, testStudyPair,
];

export const GetStudies = (payload: ISearchFilter) => {
  const [studies, setStudies] = useState<IStudyPair[]>(initialStudyPairsValue as IStudyPair[]);
  const baseUrl = process.env.REACT_APP_BASE_URL;
  const token = useRecoilValue(tokenState);
  const config = {
    headers: { "Authorization": `Bearer ${token}`}
  };

  useEffect(() => {
    const fetchStudies = () => {
      axios.post<any>(`${baseUrl}/studies`, payload, config)
      .then(response => {
        setStudies(response?.data);
      })
      .catch(error => {
        console.log(error)
      });
    };
    fetchStudies();
  }, [payload, baseUrl]);
  
  return (
    studies
  );
}
    