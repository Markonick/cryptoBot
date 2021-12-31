import React, { useEffect } from 'react';
import { useSetRecoilState } from "recoil";
import { useLocation } from "react-router-dom";
import { GetSummary } from '../../api/GetPortfolio';
import { AdequacyTable } from './AdequacyTable';
import { CriteriaTable } from './CriteriaTable';
import { Title } from './Title';
import { ISite, ISummary } from '../../customTypes';
import { summaryState } from '../../store/summaryState';

export const Summary: React.FC = () => {
  const location = useLocation<ISite>();
  const site = location.state;

  const setSummary = useSetRecoilState<ISummary>(summaryState);

  const summary = GetSummary(site.id).summary;
  setSummary(summary)
  console.log(summary)
  console.log(site)
  
  const classificationCC = summary.view_summaries.CC.positioning.classification;
  const classificationMLO = summary.view_summaries.MLO.positioning.classification;
  const criteriaCC = summary.view_summaries.CC.positioning.criteria;
  const criteriaMLO = summary.view_summaries.MLO.positioning.criteria;

  const adequacyTableCC = <AdequacyTable siteId={site.id} view={"CC"} classification={classificationCC} />;
  const adequacyTableMLO = <AdequacyTable siteId={site.id} view={"MLO"} classification={classificationMLO} />;
  const criteriaTableCC = <CriteriaTable siteId={site.id} view={"CC"} criteria={criteriaCC} />;
  const criteriaTableMLO = <CriteriaTable siteId={site.id} view={"MLO"} criteria={criteriaMLO} />;
  const totalStudies = summary.total_studies
  console.log(`NUMBER OF STUDIES FOR SITE ID ${site.id}: ${totalStudies}`, )
  const title = <Title siteName={site.name} totalStudies={totalStudies}/>;

  return (
    <div style={{color: 'black', }}>
      {title}
      <div style={{display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'left',
          flexDirection: 'row', marginLeft: 40, }}>
        <div style={{width: "35%", marginRight: 40}}>
          {adequacyTableCC}
          {criteriaTableCC}
        </div>
        <div style={{width: "35%"}}>
          {adequacyTableMLO}
          {criteriaTableMLO}
        </div>
      </div>
    </div>
  );
};

