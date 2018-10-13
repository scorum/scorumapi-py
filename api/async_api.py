import json
from . import acall


def get_result(txt):
    data = json.loads(txt)
    if "error" in data:
        print("error response: %s" % data["error"])

    if "result" not in data:
        print("wrong response format: %s" % txt)
        return None

    return data["result"]

async def get_blocks_history(url, f, limit):
    start = f + limit
    return await acall(url, "blockchain_history_api", "get_blocks_history", [start, limit])


async def get_blocks(url, f, limit):
    start = f + limit - 1
    return await acall(url, "blockchain_history_api", "get_blocks", [start, limit])


async def get_dgp(url):
    txt = await acall(url, "database_api", "get_dynamic_global_properties")
    try:
        return get_result(txt)
    except Exception as e:
        raise e
