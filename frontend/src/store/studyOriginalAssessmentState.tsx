import { atom } from "recoil";
import { recoilPersist } from 'recoil-persist';
import { IImageIdImageAssessment, IStudyAssessment } from "../customTypes";

const { persistAtom } = recoilPersist()

export const studyOriginalAssessmentState = atom<IStudyAssessment>({
  key: "studyOriginalAssessmentState",
  default: {
    study_id: -1,
    images: [] as IImageIdImageAssessment[],
  } as IStudyAssessment,
  effects_UNSTABLE: [persistAtom],
});
