import json


class Balance:
    def __init__(self, scr=0, sp=0):
        self.scr = scr
        self.sp = sp


class Account:
    name = ""
    balance = Balance()


class Genesis:
    accounts = {}
    dev_pool = Balance()
    registration_pool = 0

    def set_accounts_scr(self, accounts):
        for a in accounts:
            self.accounts[a["name"]] = Balance(scr=a["scr_amount"])

    def set_accounts_sp(self, accounts):
        for a in accounts:
            self.accounts[a["name"]] = Balance(sp=a["sp_amount"])

    def set_dev_pool(self, data):
        self.dev_pool.scr = data["development_scr_supply"]
        self.dev_pool.sp = data["development_sp_supply"]

    def set_registration_reward(self, data):
        pass

    def load(self, path):
        data = json.loads(read_file(path))

        self.set_accounts_scr(data["accounts"])
        self.set_accounts_sp(data["steemit_bounty_accounts"])
        self.set_dev_pool(data)


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def read_genesis(genesis_file="/home/alex/projects/scorum/master/genesis.json"):

    genesis = Genesis()
    genesis.load(genesis_file)


read_genesis()
