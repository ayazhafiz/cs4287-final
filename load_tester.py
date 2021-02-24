import aiohttp
import asyncio
import requests
import sys
import time
from traffic_reader import get_requests_per_second_interval

# 5 second interval
INTERVAL = 5
APP_URL = sys.argv[1]
ENDPOINT_URL = f"{APP_URL}/api/rce"

# REQUEST_COUNT = int(sys.argv[2])

async def send_request():
    data = {
        "lang":"python",
        "code":"print(\"hello there\")"
    }
    headers = {
        "Cookie": "TODO: disable auth?"
    }
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.post(ENDPOINT_URL, headers=headers, json=data) as resp:
            return (await resp.json(), time.time() - start_time)
    return None


async def main():
    start_time = time.time()
    for i, request_count in enumerate(get_requests_per_second_interval(INTERVAL)):
        tasks = [(asyncio.create_task(send_request()), j) for j in range(request_count)]
        await asyncio.sleep(INTERVAL)
        resps = [(await task, idx) for task, idx in tasks]
        average_time = sum([resp[0][1] for resp in resps])/len(resps)
        for resp in resps:
            print(f"{(i+1) * INTERVAL} seconds:", resp, f"average time: {average_time}")


start = time.time()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print(f"Took {time.time() - start} seconds to complete")
