from .protocol import UgcProtocol

from orjson import loads, dumps

from typing import Any, Optional
from asyncio import AbstractEventLoop
import asyncio


class Client:
    def __init__(
        self, protocol: Optional[Any] = None, *, loop: AbstractEventLoop = None
    ):
        if protocol:
            self.protocol = protocol
        else:
            self.protocol = UgcProtocol()
        self.events = {}
        self.loop = loop if self.loop is not None else asyncio.get_running_loop()

    async def connect(self, token: str) -> None:
        await self.protocol.connect()
        while self.protocol.open:
            data = loads(await self.protocol.recv())
            if data["type"] == "hello":
                await self.send("identify", {"token": token})
            else:
                args = []
                if data["data"] is not None:
                    args.append(data["data"])
                self.dispatch(data["type"], *args)

    def dispatch(self, type: str, *args, **kwargs):
        if type in self.events:
            for func in self.events[type]:
                self.loop.create_task(func(*args, **kwargs))

    def on(self, type: str):
        def decorator(func):
            if type in self.events:
                self.events[type].append(func)
            else:
                self.events[type] = [func]
            return func
        return decorator

    async def send(self, type: str, data: Any) -> None:
        await self.protocol.send(dumps({"type": type, "data": data}))
