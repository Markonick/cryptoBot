from dataclasses import dataclass
from typing import Optional, List

@dataclass()
class Tick:
    event_type: str
    event_time:  int
    symbol: str
    price_change: str
    price_change_percent: str
    weighted_average_price: str
    first_trade: str
    last_price: str
    last_quantity: str
    best_bid_price: str
    best_bid_quantity: str
    best_ask_price: str
    best_ask_quantity: str
    open_price: str
    high_price: str
    low_price: str
    total_traded_base_asset_volume: str
    total_traded_quote_asset_volume: str
    statistics_open_time: int
    statistics_close_time: int
    first_trade_id: int
    last_trade_id: int
    total_number_of_trades: int
    exchange: str

@dataclass
class Symbol:
    name: str
    active: bool
    
    @property
    def as_db_args(self) -> List:
        return [self.name, self.active]

@dataclass
class BinanceOrderResponse:
    symbol_id: int
    clientOrder_id: Optional[int] = None
    transactTime: Optional[int] = None
    price: Optional[float] = None
    origQty: Optional[int] = None
    executedQty: Optional[int] = None
    cummulativeQuoteQty: Optional[int] = None
    status: Optional[str] = None
    timeInForce: Optional[str] = None
    type: Optional[str] = None
    side: Optional[str] = None

    @property
    def as_db_args(self) -> List:
        return [
            self.symbol_id, self.clientOrder_id, self.transactTime, self.price, self.origQty, self.executedQty, 
            self.cummulativeQuoteQty, self.status, self.timeInForce, self.type, self.side
        ]

@dataclass
class Signal:
    symbol_id: int
    order_id: int
    value: str
    curr_rsi: float
    prev_rsi: float
    created_at: int

    @property
    def as_db_args(self) -> List:
        return [self.symbol_id, self.order_id, self.value, self.curr_rsi, self.prev_rsi, self.created_at]

@dataclass()
class OrderDetails:
    symbol_id: int
    order_id: int
    value: str
    curr_rsi: float
    prev_rsi: float
    created_at: int
    clientOrder_id: Optional[int] = None
    transactTime: Optional[int] = None
    price: Optional[float] = None
    origQty: Optional[int] = None
    executedQty: Optional[int] = None
    cummulativeQuoteQty: Optional[int] = None
    status: Optional[str] = None
    timeInForce: Optional[str] = None
    type: Optional[str] = None
    side: Optional[str] = None

@dataclass()
class Order:
    orderResponse: BinanceOrderResponse
    signalDetails: Signal
    