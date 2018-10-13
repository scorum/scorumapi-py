import api

import sys
import argparse
import logging
import json
import time

def asset_to_float(value):
    if isinstance(value, str):
        index = str(value).find(" SP")
        if index == -1:
            index = str(value).find(" SCR")
        if index > 0:
            return float(value[:index])
    return value


while True:
    response = api.call("http://127.0.0.1:8003", "chain_api", "get_chain_capital", [])

    active_voters_balancer_scr = asset_to_float(response["active_voters_balancer_scr"])
    active_voters_balancer_sp = asset_to_float(response["active_voters_balancer_sp"])


    content_balancer_scr = asset_to_float(response["content_balancer_scr"])

    content_reward_fifa_world_cup_2018_bounty_fund_sp_balance = asset_to_float(response["content_reward_fifa_world_cup_2018_bounty_fund_sp_balance"])

    content_reward_fund_scr_balance = asset_to_float(response["content_reward_fund_scr_balance"])
    content_reward_fund_sp_balance = asset_to_float(response["content_reward_fund_sp_balance"])

    dev_pool_scr_balance = asset_to_float(response["dev_pool_scr_balance"])
    dev_pool_sp_balance = asset_to_float(response["dev_pool_sp_balance"])

    fund_budget_balance = asset_to_float(response["fund_budget_balance"])

    registration_pool_balance = asset_to_float(response["registration_pool_balance"])

    total_scorumpower = asset_to_float(response["total_scorumpower"])
    total_scr = asset_to_float(response["total_scr"])

    total_supply = asset_to_float(response["total_supply"])

    total_witness_reward_scr = asset_to_float(response["total_witness_reward_scr"])
    total_witness_reward_sp = asset_to_float(response["total_witness_reward_sp"])

    witness_reward_in_sp_migration_fund = asset_to_float(response["witness_reward_in_sp_migration_fund"])

    circulating_capital = asset_to_float(response["circulating_capital"])

    t_scr = 0
    t_sp = 0

    t_scr += active_voters_balancer_scr
    t_scr += content_balancer_scr
    t_scr += content_reward_fund_scr_balance

    t_scr += dev_pool_scr_balance
    t_scr += fund_budget_balance
    t_scr += registration_pool_balance
    t_scr += total_scr

    t_sp += active_voters_balancer_sp
    t_sp += content_reward_fifa_world_cup_2018_bounty_fund_sp_balance
    t_sp += content_reward_fund_sp_balance
    t_sp += dev_pool_sp_balance
    t_sp += witness_reward_in_sp_migration_fund
    t_sp += total_scorumpower

    total = t_sp + t_scr

    if total - total_supply != 0:
        print(total)
        print(total_supply)

        print(total-total_supply)

        print(json.dumps(response, indent=4, sort_keys=True))

    time.sleep(0.5)