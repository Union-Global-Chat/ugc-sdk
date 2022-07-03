from websockets import connect
from websockets.client import WebSocketClientProtocol

from typing import Optional

from zlib import decompress, compress


class UgcProtocolError(Exception):
    pass

class UgcProtocol:
    ws: Optional[WebSocketClientProtocol] = None

    async def connect(self) -> None:
        if self.ws is None:
            self.ws = await connect("wss://ugc.renorari.net/api/v1/gateway")
        else:
            raise UgcProtocolError("Already connected")

    @property
    def open(self) -> bool:
        return self.ws.open if self.ws is not None else False

    async def recv(self) -> str:
        return decompress(await self.ws.recv())

    async def send(self, data: str) -> None:
        await self.ws.send(compress(data))