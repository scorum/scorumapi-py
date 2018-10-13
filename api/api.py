from . import call


def lookup_account_names(url, names):
    return call(url, "database_api", "lookup_account_names", [names])


def get_account_count(url):
    return call(url, "database_api", "get_account_count", [])


def lookup_accounts(url: str, start_account: str, limit: int):
    return call(url, "database_api", "lookup_accounts", [start_account, limit])


def get_discussions_by_created(url: str, query: dict):
    return call(url, "tags_api", "get_discussions_by_created", [query])


def get_ops_in_block(url, start, limit):
    return call(url, "blockchain_history_api", "get_ops_in_block", [start, limit])


def get_blocks_history(url, block_num, limit):
    start = block_num + limit
    return call(url, "blockchain_history_api", "get_blocks_history", [start, limit])


def get_ops_history(url, from_op, limit, type=0):
    return call(url, "blockchain_history_api", "get_ops_history", [from_op, limit, type])