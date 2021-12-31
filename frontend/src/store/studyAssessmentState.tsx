import { atom } from "recoil";
import { recoilPersist } from 'recoil-persist';
import { IImageIdImageAssessment, IStudyAssessment } from "../customTypes";

const { persistAtom } = recoilPersist()

export const studyAssessmentState = atom<IStudyAssessment>({
  key: "studyAssessmentState",
  default: {
    study_id: -1,
    images: [] as IImageIdImageAssessment[],
  } as IStudyAssessment,
  effects_UNSTABLE: [persistAtom],
});
