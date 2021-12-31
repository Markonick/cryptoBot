import * as React from 'react';
import { styled } from '@mui/material/styles';

const StyledRootDiv = styled('div')({
  backgroundColor: 'white',
});

export const Info: React.FC = () => {
  return (
    <>
      <StyledRootDiv>
        <h1 className="h2">INFO Stuff....</h1>
      </StyledRootDiv>
      <p>
        About
      </p>
    </>
  );
};