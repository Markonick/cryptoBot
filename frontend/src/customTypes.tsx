export enum ImageAdequacy {
  Indeterminate = "indeterminate",
  Adequate = "adequate",
  Inadequate = "inadequate",
};

export interface IAbout {
  miaIqVersion: number
  ceMarkNumber: number
};

export interface ISymbol {
  id: number
  name: string
  description: string
};

export interface IPage {
  page: number
  numberOfPages: number
};