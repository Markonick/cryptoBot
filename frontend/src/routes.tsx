// AppRoutes.tsx
import React, { Suspense } from 'react';
import { Route, Switch, withRouter } from 'react-router-dom';
import { About } from "./pages/about/About";
import { Studies } from './pages/symbols/Studies';
import { Login } from './pages/auth/Login';
import { Image } from './pages/orders/Orders';
import { Sites } from './pages/symbol/Symbol';
import { Summary } from './pages/portfolio/Portfolio';
import { AccountSettings } from './components/AccountSettings';
import { Profile } from './components/Profile';

// ======================= ROUTES CONSTANTS ================================

export const buildRoute = (route: string): string => `${route}`;

const SYMBOL_ROUTES = {
  SYMBOLS_LIST: buildRoute('/symbols'),
  SYMBOL_DETAILS: buildRoute('/symbols/:id'),
};

export const ROUTES_CONFIG = {
  ROOT: '/',
  ABOUT: '/about',
  SETTINGS: '/settings',
  PORTFOLIO: '/portfolio',
  PROFILE: '/profile',
  ...SYMBOL_ROUTES,
};

// =========================================================================

const AppRoutes: React.FC = () => {
  return (
    <Suspense fallback='loading'>
      <Switch>
        <Route path={ROUTES_CONFIG.ROOT} exact component={Sites}/>
        <Route path={ROUTES_CONFIG.PORTFOLIO} exact component={Summary}/>
        <Route path={ROUTES_CONFIG.SYMBOLS_LIST} exact component={Studies}/>
        <Route path={ROUTES_CONFIG.ABOUT} exact component={About}/>
        <Route path={ROUTES_CONFIG.SETTINGS} exact component={AccountSettings}/>
        <Route path={ROUTES_CONFIG.PROFILE} exact component={Profile}/>
      </Switch>
    </Suspense>
  );
};

export default withRouter(AppRoutes);