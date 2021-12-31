import React from 'react';
import { useRecoilValue } from "recoil";
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles'
import { Header } from './components/Header';
import AppRoutes from "./routes";
import { lightTheme, darkTheme } from './theme';
import './App.css';
import { themeState } from './store/themeState';

function App() {
  const themeFlag = useRecoilValue(themeState);
  const theme = themeFlag === 'dark' ? darkTheme : lightTheme;

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Header />
        <div style={{
          position: 'relative',
          minHeight: '100vh',
          marginTop: 0,
        }}>
          <div className="row"
          >
            <main
              role="main"
              className="col-md-9 ml-sm-auto col-lg-10 px-md-4"
            >
              <AppRoutes />
            </main>
          </div>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
