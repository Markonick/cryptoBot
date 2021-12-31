import { atom } from "recoil";
import { recoilPersist } from 'recoil-persist';
import { IPage } from "../customTypes";

const { persistAtom } = recoilPersist()

export const pageState = atom<IPage>({
  key: "pageState",
  default: {
    page: 1,
    numberOfPages: 3,
  } as IPage,
  effects_UNSTABLE: [persistAtom],
});
