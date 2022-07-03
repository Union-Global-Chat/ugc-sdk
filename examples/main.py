from ugc_sdk import Client

import asyncio

async def main():
    client = Client(loop=asyncio.get_running_loop())
    await client.connect("token")

asyncio.run(main())