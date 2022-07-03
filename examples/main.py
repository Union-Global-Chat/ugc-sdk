from ugc_sdk import Client

import asyncio
from os import getenv

async def main():
    client = Client(loop=asyncio.get_running_loop())
    await client.connect(getenv("token"))

asyncio.run(main())