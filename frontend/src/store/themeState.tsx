import { atom } from "recoil";
import { recoilPersist } from 'recoil-persist';

const { persistAtom } = recoilPersist()

export const themeState = atom<string>({
  key: "themeState",
  default: 'light',
  effects_UNSTABLE: [persistAtom],
});
