import typing, time, json, os, asyncio
from typing import Optional, NewType
from fastapi import FastAPI, WebSocket, Depends, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.responses import HTMLResponse, UJSONResponse, PlainTextResponse
from starlette.endpoints import WebSocketEndpoint
from starlette.middleware.cors import CORSMiddleware

import asyncpg

# from .repositories import KafkaTickerRepository
from repositories import KafkaTickerRepository
from services import TickerService

KAFKA_ADVERTISED_HOST_NAME = os.environ.get("KAFKA_ADVERTISED_HOST_NAME")
KAFKA_TICKER_TOPIC = os.environ.get("KAFKA_TICKER_TOPIC")
KAFKA_KLINES_TOPIC = os.environ.get("KAFKA_KLINES_TOPIC")
API_BASE_URL = os.environ.get("API_BASE_URL")

app = FastAPI()
router = InferringRouter()
app.add_middleware(CORSMiddleware, allow_origins=["*"])
loop = asyncio.get_event_loop()

ticker_service = TickerService(KafkaTickerRepository(loop, KAFKA_KLINES_TOPIC, KAFKA_ADVERTISED_HOST_NAME), 1)
@cbv(router)
class KlinesRoute:
    @router.get(f"{API_BASE_URL}/klines")
    async def get_klines(symbol: str) -> str:
        topic = KAFKA_KLINES_TOPIC
        # await svc.(topic, symbol)

@cbv(router)
class TickerRoute:
    def __init__(self):
        self._ticker_service = ticker_service

    @router.websocket("/ws/tickers/{symbol}")
    async def websocket_endpoint(self, websocket: WebSocket, symbol: str) -> None:
        await websocket.accept()
        msg = {"Message: ": "connected"}
        await websocket.send_json(msg)
        tick = await self._ticker_service.get_ticker(symbol)
        await websocket.send_text(tick)

app.include_router(router)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(create_pool()) 