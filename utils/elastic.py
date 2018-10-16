import argparse
import time
import json
import multiprocessing as mp
from elasticsearch import Elasticsearch
from progressbar import ProgressBar

from api import helpers
from api import api


URL_ELASTIC = "blockchain-dnt-vm-a-1.scorum.com:9200"
#URL_ELASTIC = "h2-de.scorum.com:9200"
#URL_RPC = "http://rpc5-mainnet-weu-v2.scorum.com:8001/rpc"
URL_RPC = "http://127.0.0.1:8021/rpc"
# URL_RPC = "https://prodnet.scorum.com/rpc"


asset_fields = ("author_payout_scr_value",
                "author_payout_sp_value",
                "beneficiary_payout_scr_value",
                "beneficiary_payout_sp_value",
                "curator_payout_scr_value",
                "curator_payout_sp_value",
                "from_children_payout_scr_value",
                "from_children_payout_sp_value",
                "to_parent_payout_scr_value",
                "to_parent_payout_sp_value",
                "total_payout_scr_value",
                "total_payout_sp_value",
                "max_accepted_payout",
                "promoted",
                "pending_payout_scr",
                "pending_payout_sp")

int_fields = ("body_length",
              "children",
              "abs_rshares",
              "net_rshares",
              "net_votes",
              "children_abs_rshares",
              "total_vote_weight",
              "vote_rshares",
              "depth",
              "id",
              "root_comment")


def asset_to_float(value):
    if isinstance(value, str):
        if value[-2:] == "SP" or value[-3:] == "SCR":
            index = str(value).find(" SP")

            if index == -1:
                index = str(value).find(" SCR")

            if index > 0:
                try:
                    return float(value[:index])
                except:
                    return value

    return value


def to_account(a):
    a["owner"] = ""
    a["active"] = ""
    a["posting"] = ""
    a["memo"] = ""

    for key, value in a.items():
        a[key] = asset_to_float(value)

    return a


def to_comment(c):
    for key, value in c.items():
        if key in asset_fields:
            c[key] = asset_to_float(value)
        elif key in int_fields:
            c[key] = int(value)

    return c


def elastic_push(account):
    es = Elasticsearch(URL_ELASTIC, maxsize=25)
    res = es.index(index="accounts", doc_type='accounts', id=account["id"], body=to_account(account))


def elastic_push_comment(comment):
    try:
        es = Elasticsearch(URL_ELASTIC, maxsize=25)
        res = es.index(index="comments", doc_type='comments', id=comment["id"], body=to_comment(comment))
    except Exception as e:
        print("---------------")
        print(json.dumps(comment))
        print(e)
        print("---------------")


def elastic_posts(rpc_url, elastic_url):
    print("start sync posts")
    start = time.time()

    posts = helpers.get_all_posts(rpc_url)

    print("getting posts objects took: %s s" % (time.time() - start))

    with mp.Pool() as p:
        with ProgressBar(maxval=len(posts)) as pbar:
            for i in enumerate(p.imap_unordered(elastic_push_comment, posts)):
                pbar.update(pbar.value + 1)

    print("pushing posts took: %s s" % (time.time() - start))


def elastic_accounts(rpc_url, elastic_url):
    print("start sync accounts")
    start = time.time()

    p = mp.Pool()

    pbar = ProgressBar(maxval=api.get_account_count(rpc_url))

    def callback(accounts):
        for i in enumerate(p.imap_unordered(elastic_push, accounts)):
            if pbar.value < pbar.max_value:
                pbar.update(pbar.value + 1)

    helpers.scan_accounts(rpc_url, callback)

    print("pushing accounts took: %s s" % (time.time() - start))


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-v", dest='verbose', default=False, action='store_true', help='')
    parser.add_argument('--elastic', dest='elastic', action='store', default=URL_ELASTIC, help='')
    parser.add_argument('--rpc', dest='rpc', action='store', default=URL_RPC, help='')
    parser.add_argument('-j,--jobs', dest='jobs', nargs='*', action='store', default=[], help='')

    opt = parser.parse_args()

    if "posts" in opt.jobs:
        elastic_posts(opt.rpc, opt.elastic)

    if "accounts" in opt.jobs:
        elastic_accounts(opt.rpc, opt.elastic)


def test_xxx():
    ss = "0.00000 SP"

    assert ss[-2:] == "SP"