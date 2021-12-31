import { selector } from 'recoil';
import { siteState } from './siteState';

export const getSite = selector({
  key: 'GetSite',
  get: ({get}) => get(siteState),
})