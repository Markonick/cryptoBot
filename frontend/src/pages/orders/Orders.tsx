import * as React from 'react';
import { AboutCard } from '../about/AboutCard';


export const Orders: React.FC = () => {
  const about = { miaIqVersion: 0, ceMarkNumber: 0 }
  return (
    <>
      <AboutCard about={about} />
    </>
  );
};