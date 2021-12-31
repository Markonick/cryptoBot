import * as React from 'react';
import { AboutCard } from './AboutCard';


export const About: React.FC = () => {
  const about = {miaIqVersion: 0, ceMarkNumber: 0}
  return (
    <>
      <AboutCard about={about}/>
    </>
  );
};