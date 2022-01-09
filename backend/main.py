import typing, time, json, os, asyncio
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import FastAPI, WebSocket, Depends, status
from starlette.websockets import WebSocketDisconnect
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.middleware.cors import CORSMiddleware
import pika
import asyncpg

from repositories import RabbitMqTickerRepository
from services import TickerService
from notifier import Notifier


SCHEMA = os.environ.get("SCHEMA")
EXCHANGE = os.environ.get("RABBITMQ_EXCHANGE")
HOST = os.environ.get("RABBITMQ_HOST")
PORT = os.environ.get("RABBITMQ_PORT")
QUEUE = os.environ.get("RABBITMQ_QUEUE")
RABBITMQ_KLINES_TOPIC = os.environ.get("RABBITMQ_KLINES_TOPIC")
API_BASE_URL = os.environ.get("API_BASE_URL")

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
notifier = Notifier()
config={'exchange': EXCHANGE, 'host': HOST, 'port': PORT}

@app.post("/symbols")
async def push_to_connected_websockets(symbols: List[str]):
    print("symbols")
    print(symbols)
    if not notifier.is_ready:
        await notifier.setup(symbols)
    await notifier.push(f"! Push notification: {symbols} !")

@app.websocket("/ws/tickers/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str) -> None:
    await notifier.connect(websocket)
    try:
        print('In Webscoket endpoint try')
        while True:
            data = await websocket.receive_text()
            # print(data)
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("WebSocketDisconnect!!")
        print("WebSocketDisconnect!!")
        print("WebSocketDisconnect!!")
        notifier.remove(websocket)
