methods = {
    "get_dynamic_global_properties": "database_api",
    "get_account_count": "database_api",
    "lookup_account_names": "database_api",
    "lookup_accounts": "database_api",
    "get_witnesses": "database_api",

    "get_trending_tags": "tags_api",
    "get_tags_used_by_author": "tags_api",
    "get_tags_by_category": "tags_api",
    "get_discussions_by_trending": "tags_api",
    "get_discussions_by_created": "tags_api",
    "get_discussions_by_hot": "tags_api",
    "get_discussions_by_author": "tags_api",
    "get_content": "tags_api",
    "get_comments": "tags_api",

    "get_stats_for_time": "blockchain_statistics_api",
    "get_stats_for_interval": "blockchain_statistics_api",
    "get_lifetime_stats": "blockchain_statistics_api",

    "get_ops_history": "blockchain_history_api",
    "get_ops_history_by_time": "blockchain_history_api",
    "get_ops_in_block": "blockchain_history_api",
    "get_transaction": "blockchain_history_api",
    "get_block_header": "blockchain_history_api",
    "get_block_headers_history": "blockchain_history_api",
    "get_block": "blockchain_history_api",
    "get_blocks_history": "blockchain_history_api",

    "get_chain_capital": "chain_api"}


def get_api_name(method):
    try:
        api = methods[method]
        return api
    except:
        return None


def to_payload(method, api="", args=[]):
    if api is "" or api is None:
        api = get_api_name(method)
        if api is "" or api is None:
            raise Exception('there is no api for method: %s' % method)

    data = dict()

    data["id"] = "0"
    data["jsonrpc"] = "2.0"
    data["method"] = "call"

    data["params"] = [api, method, args]

    return data
