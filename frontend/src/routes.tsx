import React, { Suspense } from 'react';
import { useRoutes } from "react-router-dom";
import { About } from "./pages/about/About";
import { Portfolio } from './pages/portfolio/Portfolio';
import { Symbols } from './pages/symbols/Symbols';
import { AccountSettings } from './components/AccountSettings';
import { Profile } from './components/Profile';
import { Orders } from './pages/orders/Orders';

// ======================= ROUTES CONSTANTS ================================

export const buildRoute = (route: string): string => `${route}`;

const SYMBOL_ROUTES = {
  SYMBOLS: buildRoute('/symbols'),
  SYMBOL: buildRoute('/symbols/:id'),
};

export const ROUTES_CONFIG = {
  ROOT: '/',
  ABOUT: '/about',
  SETTINGS: '/settings',
  PORTFOLIO: '/portfolio',
  ORDERS: '/orders',
  PROFILE: '/profile',
  ...SYMBOL_ROUTES,
};

// =========================================================================

const routes = [
  { path: ROUTES_CONFIG.ROOT, element: <Portfolio /> },
  { path: ROUTES_CONFIG.PORTFOLIO, element: <Portfolio /> },
  { path: ROUTES_CONFIG.ORDERS, element: <Orders /> },
  { path: ROUTES_CONFIG.SYMBOLS, element: <Symbols /> },
  { path: ROUTES_CONFIG.ABOUT, element: <About /> },
  { path: ROUTES_CONFIG.SETTINGS, element: <AccountSettings /> },
  { path: ROUTES_CONFIG.PROFILE, element: <Profile /> },
]

const AppRoutes: React.FC = () => {

  const routeResult = useRoutes(routes);
  return (
    <Suspense fallback='loading'>
      {routeResult}
    </Suspense>
  );
};

export default AppRoutes;