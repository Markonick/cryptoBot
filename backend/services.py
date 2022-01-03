from typing import List
from abc import ABC, abstractmethod
from entities import Tick
from repositories import ITickerRepository

TickBuffer = List[int]


class ITickerService(ABC):
    @abstractmethod
    async def get_ticker(self, symbol: str) -> Tick:
        pass

class TickerService:
    """
    Window is global throughout all symbols. If I change window,  Iwant to see the same price change
    among all cryptos in the list, on the UI. Hence we initialise this service with window
    """
    def __init__(self, repo: ITickerRepository, window: int) -> None:
        self._window = window
        self._repo = repo

    async def get_ticker(self, symbol: str) -> Tick:
        print('GET TICKER')
        tick = await self._repo.get_ticker_by_window()
        return tick
        
    def get_is_price_up(self, incomingTick: Tick) -> bool:
        return incomingTick.price > self._get_bufferedTick(self._window).price

    def _get_bufferedTick(self, window: int) -> Tick:
        tick = self._repo.get_tick_by_window(window)
        return tick
