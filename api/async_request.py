import aiohttp
import asyncio
import json

from api.methods import get_api_name, to_payload


async def acall(url, api, method, args=[], retries=5):
    payload = to_payload(method, api, args)

    for i in range(0, retries):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status == 200:
                    i = retries
                    # print("request: %s" % json.dumps(payload))
                    data = await resp.content.read()
                    try:
                        return data.decode("utf-8")
                    except Exception as e:
                        print("error: %s" % str(e))
                        print("request: %s" % json.dumps(payload))
                        print("response: " + data)

                else:
                    print("error during request")
                    asyncio.sleep(0.5)
