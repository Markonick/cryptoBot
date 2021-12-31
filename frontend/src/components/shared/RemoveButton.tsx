import React from 'react';
import { styled } from '@mui/material/styles';
import CloseIcon from '@mui/icons-material/Close';

const StyledRootDiv = styled('div')({
  width: 10,
  height: 10,
  color: "gray",
  fontWeight: 200,
  '&:hover': {
    color: "black",
    opacity: 0.7,
    cursor: 'pointer',
  },
});

interface IButtonProps {
    children?: React.ReactNode;
    props?: any;
    onClick?: any;
}

export const RemoveButton: React.FC<IButtonProps> = ({ onClick, children, ...props }) => {

  return (
    <StyledRootDiv>
      <CloseIcon fontSize='small' onClick={onClick} />
    </StyledRootDiv>
  )
};
