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

export interface ITick {
  event_type: string
  event_time: number
  symbol: string
  price_change: string
  price_change_percent: string
  weighted_average_price: string
  first_trade: string
  last_price: string
  last_quantity: string
  best_bid_price: string
  best_bid_quantity: string
  best_ask_price: string
  best_ask_quantity: string
  open_price: string
  high_price: string
  low_price: string
  total_traded_base_asset_volume: string
  total_traded_quote_asset_volume: string
  statistics_open_time: number
  statistics_close_time: number
  first_trade_id: number
  last_trade_id: number
  total_number_of_trades: number
  exchange: string
};