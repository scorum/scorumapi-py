from .request import call


def lookup_account_names(url, names):
    return call(url, "database_api", "lookup_account_names", names)


def get_account_count(url):
    return call(url, "database_api", "get_account_count", [])


def lookup_accounts(url: str, start_account: str, limit: int):
    return call(url, "database_api", "lookup_accounts", [start_account, limit])


def get_discussions_by_created(url: str, query: dict):
    return call(url, "tags_api", "get_discussions_by_created", [query])
