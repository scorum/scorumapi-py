import argparse
import time
import os
import multiprocessing as mp
from elasticsearch import Elasticsearch
from progressbar import ProgressBar

from api import helpers
from api import api


URL_ELASTIC = "blockchain-dnt-vm-a-1.scorum.com:9200"
URL_RPC = "http://blockchain-dnt-vm-a-2.scorum.com:8001/rpc"
# URL_RPC = "https://prodnet.scorum.com/rpc"


def asset_to_float(value):
    if isinstance(value, str):
        index = str(value).find(" SP")

        if index == -1:
            index = str(value).find(" SCR")

        if index > 0:
            return float(value[:index])

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
        c[key] = asset_to_float(value)

    return c


def elastic_push(account):
    es = Elasticsearch(URL_ELASTIC, maxsize=25)
    res = es.index(index="scorum", doc_type='accounts', id=account["id"], body=to_account(account))


def elastic_push_comment(comment):
    es = Elasticsearch(URL_ELASTIC, maxsize=25)
    res = es.index(index="scorum2", doc_type='comments', id=comment["id"], body=to_comment(comment))


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
    parser.add_argument('--jobs', dest='jobs', nargs='*', action='store', default=[], help='')

    opt = parser.parse_args()

    if "posts" in opt.jobs:
        elastic_posts(opt.rpc, opt.elastic)

    if "accounts" in opt.jobs:
        elastic_accounts(opt.rpc, opt.elastic)
