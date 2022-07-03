from ugc_sdk import Client

import asyncio
from os import getenv

async def main():
    client = Client(loop=asyncio.get_running_loop())
    await client.connect(getenv("token"))

    @client.on("identify")
    async def login():
        print("Logged in")

asyncio.run(main())