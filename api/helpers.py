from api import api


def get_all_account_names(url):
    accounts = []
    stop = False
    start_account = ""

    while stop is not True:

        r = api.lookup_accounts(url, start_account, 100)

        if len(accounts) == 0:
            accounts += r
        else:
            accounts += r[1:]

        if start_account == accounts[-1]:
            stop = True

        start_account = accounts[-1]

    assert api.get_account_count(url) == len(accounts)

    return accounts


def get_all_account_objects(url):
    all_account_names = get_all_account_names(url)
    r = api.lookup_account_names(url, [all_account_names])

    assert len(r) == api.get_account_count(url)

    return r


def get_all_posts(url):
    query = dict()
    query["limit"] = 100

    posts = []

    stop = False

    while stop is not True:
        r = api.get_discussions_by_created(url, query)

        if len(posts) != 0 and query["start_author"] == r[-1]["author"] and query["start_permlink"] == r[-1]["permlink"]:
            stop = True

        if len(posts) == 0:
            posts += r
        else:
            posts += r[1:]

        query["start_author"] = posts[-1]["author"]
        query["start_permlink"] = posts[-1]["permlink"]

    return posts
