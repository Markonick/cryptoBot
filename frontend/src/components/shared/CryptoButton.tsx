import React from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';

const DEFAULT_SIZE = [80, 40];
const DEFAULT_FONTSIZE = 12;

const StyledButton = styled(Button)({
  width: DEFAULT_SIZE[0],
  height: DEFAULT_SIZE[1],
  backgroundColor: "#62D7C5",
  color: "inherit",
  border: "1px solid inherit",
  fontSize: DEFAULT_FONTSIZE,
  fontWeight: 200,
  '&:hover': {
    background: 'inherit',
    border: "1px solid aqua",
    color: "black",
    opacity: 0.7,
  },
});

interface IButtonProps {
    children?: React.ReactNode;
    text: string;
    disabled?: boolean;
    onClick?: any;
    width?: number;
    height?: number;
    color?: string;
    backgroundColor?: string;
}

export const KheironButton: React.FC<IButtonProps> = (props:IButtonProps) => {
  const { color, backgroundColor, width=DEFAULT_SIZE[0], height=DEFAULT_SIZE[1], onClick, text, disabled=false } = props;
  // const derivedFontsize = Math.floor(DEFAULT_FONTSIZE * (width / DEFAULT_SIZE[0]))

  return (
    <StyledButton variant="text" disabled={disabled} onClick={onClick} style={{width: width , height: height, fontSize:9, backgroundColor: backgroundColor, color: color,
    }}>
      {text}
    </StyledButton>
  )
};
