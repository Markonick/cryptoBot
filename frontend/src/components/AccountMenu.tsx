import * as React from 'react';
import { useHistory } from 'react-router-dom';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { makeStyles, useTheme } from "@mui/styles";
import ListItemIcon from '@mui/material/ListItemIcon';
import SettingsIcon from '@mui/icons-material/Settings';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import Logout from '@mui/icons-material/Logout';
import { ROUTES_CONFIG } from '../routes';
import { Theme } from '@mui/system';

const colorArray = ["crimson", "pink", "springgreen", "orange"];
const getRandomColor = () => colorArray[Math.floor(Math.random() * colorArray.length)];

const useStyles = makeStyles(({
  link: {
    fontSize: 11,
    fontStyle: "normal",
    fontWeight: 200,
    fontFamily: "Helvetica",
    textTransform: 'uppercase',
    letterSpacing: '1px',
    lineHeight: '1.3em',
    WebkitFontSmoothing: 'antialiased',
    display: "flex",
    flexDirection: "row",
    transition: '1s',
    "&:hover": {
      color: getRandomColor(),
      transition: "0.7s",
    },
    "&:focus": {
      color: getRandomColor(),
      transition: "0.7s",
    }
  },
}));

interface AccountProps {
    account: any
		color: any
};

export const AccountMenu: React.FC<AccountProps> = (props:AccountProps) => {
  const classes = useStyles();
  const history = useHistory();
  const theme = useTheme() as Theme;
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
	const initials = `${props.account?.name[0].toUpperCase()}${props.account?.name[1].toUpperCase()}`;

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };
	
	const handleMenuItemClick = (route:string) => {
    history.push(route, {account: props.account});
	};

  return (
    <React.Fragment>
      <Box sx={{ display: 'flex', alignItems: 'center', textAlign: 'center' }}>
        <Tooltip title="Account settings">
          <IconButton onClick={handleClick} size="small" sx={{ ml: 2 }}>
            <Avatar sx={{ width: 32, height: 32, bgcolor: props.color, fontSize: 11, }}>{initials}</Avatar>
          </IconButton>
        </Tooltip>
      </Box>
      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        onClick={handleClose}
        PaperProps={{
          elevation: 0,
          sx: {
            overflow: 'visible',
            filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
            mt: 1.5,
            '& .MuiAvatar-root': {
              width: 32,
              height: 32,
              ml: -0.5,
              mr: 1,
            },
            '&:before': {
              content: '""',
              display: 'block',
              position: 'absolute',
              top: 0,
              right: 14,
              width: 10,
              height: 10,
              bgcolor: 'background.paper',
              transform: 'translateY(-50%) rotate(45deg)',
              zIndex: 0,
            },
          },
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <MenuItem onClick={() => handleMenuItemClick(ROUTES_CONFIG.PROFILE)}>
          <Avatar />
					<div className={classes.link} style={{color: theme.palette.primary.text}}>Profile</div>
        </MenuItem>		
        <MenuItem onClick={() => handleMenuItemClick(ROUTES_CONFIG.ROOT)}>
          <Avatar />
					<div className={classes.link} style={{color: theme.palette.primary.text}}>My account</div>
        </MenuItem>
        <Divider />
        <MenuItem onClick={() => handleMenuItemClick(ROUTES_CONFIG.SETTINGS)}>
          <ListItemIcon>
            <SettingsIcon fontSize="medium"/>
          </ListItemIcon>
					<div className={classes.link} style={{color: theme.palette.primary.text}}>Settings</div>
        {/* <ThemeSwitch/> */}
        </MenuItem>
        <MenuItem onClick={() => handleMenuItemClick(ROUTES_CONFIG.AUTH_LOGIN)}>
          <ListItemIcon>
            <Logout fontSize="medium" />
          </ListItemIcon>
					<div className={classes.link} style={{color: theme.palette.primary.text}}>Logout</div>
        </MenuItem>
      </Menu>
    </React.Fragment>
  );
}
