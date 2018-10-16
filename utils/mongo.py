import argparse
import json
import logging
import yaml
import pymongo

from datetime import datetime

from api import helpers

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

date_fields = ("active", "created", "cashout_time", "last_payout", "last_update")


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


def string_to_date(value):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")


def mongo_posts(config):
    print("start sync posts")

    posts = helpers.get_all_posts(config['node'][0])

    for i in range(0, len(posts)):
        posts[i]["json_metadata"] = json.loads(posts[i]["json_metadata"])

        for key, value in posts[i].items():
            if key in date_fields:
                posts[i][key] = string_to_date(value)
            if key in asset_fields:
                posts[i][key] = asset_to_float(value)

    if config['dump_to_file'] is not None:
        with open(config['dump_to_file'], 'w') as file:
            file.write(json.dumps(posts))

    myclient = pymongo.MongoClient("mongodb://{}/".format(config['mongodb']))
    mydb = myclient["scorum"]
    mycol = mydb["posts"]

    mycol.drop()
    mycol.insert_many(posts)


def configure_logger(config):
    if config['level'] == 'debug':
        logging.getLogger().setLevel(logging.DEBUG)
    elif config['level'] == 'info':
        logging.getLogger().setLevel(logging.INFO)
    elif config['level'] == 'error':
        logging.getLogger().setLevel(logging.ERROR)
    elif config['level'] == 'critical':
        logging.getLogger().setLevel(logging.CRITICAL)
    elif config['level'] == 'off':
        logging.getLogger().setLevel(logging.NOTSET)


def default_config():
    return {'mongodb': '127.0.0.1:27017',
            'start_author': None,
            'start_permlink': None,
            'limit': 100,
            'dump_to_file': None,
            'logger': {'level': 'info', 'file': 'log.txt'},
            'node': ['http://127.0.0.1:8031']}


def get_config(args):
    import os

    if args.config is not None:
        config_file = args.config

        if not os.path.exists(config_file):
            raise FileExistsError("config file {} does not exists.".format(config_file))
    else:
        config_file = os.getcwd() + "/" + "config.yml"
        if not os.path.exists(config_file):
            config_file = None

    if config_file is not None:
        logging.info("loading config file {}".format(config_file))
        with open(config_file, "r") as file:
            d = file.read()
            return yaml.load(d)

    return default_config()


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-6s %(name)-12s %(message)s')

    parser = argparse.ArgumentParser(description='gather posts from blockchain node to the mongodb.')
    parser.add_argument('--version', action='store_true', help='Show version information')
    parser.add_argument('-c', '--config', action='store', help='Path to config file')

    args = parser.parse_args()

    config = get_config(args)

    configure_logger(config['logger'])

    mongo_posts(config)
