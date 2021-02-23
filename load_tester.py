import aiohttp
import asyncio
import requests
import sys
import time

APP_URL = sys.argv[1]
ENDPOINT_URL = f"{APP_URL}/api/rce"

REQUEST_COUNT = int(sys.argv[2])

async def send_request():
    data = {
        "lang":"python",
        "code":"print(\"hello there\")"
    }
    headers = {
        "Cookie": "TODO: disable auth?"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(ENDPOINT_URL, headers=headers, json=data) as resp:
            return resp
    return None


async def main():
    tasks = [(asyncio.create_task(send_request()), i) for i in range(REQUEST_COUNT)]
    resps = [(await task, idx) for task, idx in tasks]
    for resp in resps:
        print(resp)


start = time.time()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print(f"Took {time.time() - start} seconds to complete")
