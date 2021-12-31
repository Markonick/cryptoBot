import { atom } from "recoil";
import { recoilPersist } from 'recoil-persist';
import { ICriterionAssessment, IImageIdImageAssessment, ImageAdequacy, IImageAssessment } from "../customTypes";

const { persistAtom } = recoilPersist()

export const imageIdImageAssessmentState = atom<IImageIdImageAssessment>({
  key: "imageIdImageAssessmentState",
  default: {
    id: -1,
    assessment: {
      adequate: ImageAdequacy.Indeterminate,
      criteria: [] as ICriterionAssessment[]
    } as IImageAssessment,
  } as IImageIdImageAssessment,
  // effects_UNSTABLE: [persistAtom],
});
