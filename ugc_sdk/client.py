from .protocol import UgcProtocol

from orjson import loads, dumps

from typing import Any, Optional
from asyncio import AbstractEventLoop


class Client:
    def __init__(
        self, protocol: Optional[Any] = None, loop: AbstractEventLoop
    ):
        if protocol:
            self.protocol = protocol
        else:
            self.protocl = UgcProtocol()
        self.events = {}
        self.loop = loop

    async def connect(self, token: str) -> None:
        await self.protocol.connect()
        while self.protocol.opened:
            data = loads(await self.protocol.recv())
            if data["type"] == "hello:
                await self.send("identify", {"token": token})
            else:
                for func in self.events[data["type"]]:
                    self.loop.create_task(func(data["data"]))

    def on(self, type):
        def decorator(func):
            if type in self.events:
                self.events[type].append(func)
            else:
                self.events[type] = func
            return func
        return decorator

    async def send(self, type: str, data: Any) -> None:
        await self.protocol.send(dumps({"type": type, "data": data}))