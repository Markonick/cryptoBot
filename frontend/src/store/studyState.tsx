import { atom } from "recoil";
import { recoilPersist } from 'recoil-persist';
import { IStudy } from '../customTypes';

const { persistAtom } = recoilPersist()

export const studyState = atom<IStudy>({
  key: "studyState",
  default: {} as IStudy,
  effects_UNSTABLE: [persistAtom],
});
