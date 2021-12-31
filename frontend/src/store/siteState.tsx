import { atom, selector } from "recoil";
import { recoilPersist } from 'recoil-persist';
import { ISite } from '../customTypes';

const { persistAtom } = recoilPersist()

export const siteState = atom<ISite>({
  key: "siteState",
  default: {} as ISite,
  effects_UNSTABLE: [persistAtom],
});

// export const cartTotal = selector<number>({
//   key: 'cartTotal',
//   get: ({get}) => get(cartState).reduce((a, b) => a + b.organization_id, 0),
// })