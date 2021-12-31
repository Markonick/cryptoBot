import { atom } from "recoil";
import { recoilPersist } from 'recoil-persist';
import { ISwitch } from "../customTypes";

const { persistAtom } = recoilPersist()

export const switchesState = atom<ISwitch>({
  key: "switchesState",
  default: {
    annotations: true,
    priors: false,
    hasPriors: false,
  },
  // effects_UNSTABLE: [persistAtom],
});
