import React from 'react';
import { useLocation, useHistory } from "react-router-dom";
import { createStyles, makeStyles } from '@mui/styles';
import { Laterality } from '../../customTypes';

const useStyles = makeStyles(() =>
  createStyles({
    root: {
      display: 'flex',
      flexWrap: 'wrap',
      justifyContent: 'center',
      overflowY: "auto",
      overflowX: "hidden",
    },
    img:{
      width: '100%',
      transition: '1s',
    },
    textOnImage:{
      color: 'aqua',
    },
    container: {
      // position: 'relative',
      "&:hover": {
        color: 'aqua',
        '& $overlay':{
          opacity: 1,
          transition: "0.7s",
      // width: 200,
        },
        '& $img':{
          opacity: 1,
          transition: "0.7s",
        },
        '& $textOnImage':{
          opacity: 1,
        }
      },
    },
    overlay: {
      width: '100%',
      height: 100,
      position: 'absolute',
      top: 0,
      left:0,
      background: 'rgba(0, 0, 0, 0.1)',
      transition: '.5s ease',
      opacity:0,
      fontStyle: 'normal',
      fontWeight: 100,
      textAlign: 'left',
      margin: 10,
      fontFamily: "Quicksand",
    },
    icon: {
      color: 'rgba(255, 255, 255, 0.34)',
    },
    background: {
      position: 'relative',
      objectFit: 'cover',
      paddingTop: 0,
      margin: 0
    },
    overlay2: {
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      margin: 0,
      backgroundColor: 'inherit'
    },
  }),
);

export const Image: React.FC = () => {
  const classes = useStyles();
  const history = useHistory();
  const location = useLocation<any>();
  const image = location.state.image;
  const isAnnotationsOn = location.state.isAnnotationsOn;
  const isPriors = location.state.isPriors;
  
  return (
    <div > 
      <div className={classes.background}>
        <img src={image.original_png.url} alt={image.original_png.url} className={classes.overlay2} 
          style={{transform: image.laterality === Laterality.RIGHT ? 'scaleX(-1)' : ""}}
          onClick={history.goBack}
        /> 
        {isAnnotationsOn && !isPriors ? 
        <img
          src={`${image.segmentation_svg.url}`}
          alt={image.segmentation_svg.url} 
          style={{transform: image.laterality === Laterality.RIGHT ? 'scaleX(-1)' : ""}}
          loading="lazy"
          className={classes.overlay2}
          onClick={history.goBack}
        /> : "" }
        <div className={classes.overlay}>
          <p className={classes.textOnImage}>
            <span style={{color: 'white'}}>UID:</span>  {image.uid}
          </p>
          <div className={classes.textOnImage} style={{wordWrap: 'break-word'}}>
            <span style={{color: 'white'}}>View-Laterality: </span> {image.view}-{image.laterality}
           </div>
          <p className={classes.textOnImage}>
          <span style={{color: 'white'}}>url: </span>{image.preview_png.url} <br />
          </p>
          <p className={classes.textOnImage}>
            <span style={{color: 'white'}}>Compression: </span> {image.compression}
          </p>
        </div>
      </div>     
    </div>
  );
}