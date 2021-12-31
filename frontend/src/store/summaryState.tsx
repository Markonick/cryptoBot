import { atom, selector } from "recoil";
import { recoilPersist } from 'recoil-persist';
import { ISummary } from '../customTypes';

const { persistAtom } = recoilPersist()

export const summaryState = atom<ISummary>({
  key: "summaryState",
  default: {} as ISummary,
  effects_UNSTABLE: [persistAtom],
});

// export const cartTotal = selector<number>({
//   key: 'cartTotal',
//   get: ({get}) => get(cartState).reduce((a, b) => a + b.organization_id, 0),
// })