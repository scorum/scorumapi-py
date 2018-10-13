import subprocess
import json


def test_get_dynamic_global_properties():
    response = subprocess.Popen("scorumapi --no-color", shell=True, stdout=subprocess.PIPE).stdout.read()

    data = json.loads(response.decode("utf-8"))

    fields = ("average_block_size",
              "circulating_capital",
              "content_reward_scr_balance",
              "content_reward_sp_balance",
              "current_aslot",
              "current_reserve_ratio",
              "current_witness",
              "fund_budget_balance",
              "head_block_id",
              "head_block_number",
              "id",
              "last_irreversible_block_num",
              "majority_version",
              "max_virtual_bandwidth",
              "participation_count",
              "recent_slots_filled",
              "registration_pool_balance",
              "reward_pool_balance",
              "time",
              "total_pending_scr",
              "total_pending_sp",
              "total_scorumpower",
              "total_supply",
              "total_witness_reward_scr",
              "total_witness_reward_sp")

    for field in fields:
        assert field in data, "Required field is not in the response '%s'" % field


def test_lookup_account_names():
    response = subprocess.Popen("scorumapi --no-color --method lookup_account_names --args kotik", shell=True, stdout=subprocess.PIPE).stdout.read()

    data = json.loads(response.decode("utf-8"))

    fields = ("active_sp_holders_pending_scr_reward",
              "json_metadata",
              "active",
              "owner",
              "posting",
              "delegated_scorumpower",
              "last_root_post",
              "recovery_account",
              "vote_count",
              "scorumpower",
              "memo_key",
              "balance",
              "last_owner_update",
              "created",
              "lifetime_bandwidth",
              "comment_count",
              "post_count",
              "id",
              "curation_rewards_sp",
              "curation_rewards_scr",
              "can_vote",
              "owner_challenged",
              "last_post",
              "witnesses_voted_for",
              "received_scorumpower",
              "lifetime_market_bandwidth",
              "posting_rewards_sp",
              "active_challenged",
              "average_market_bandwidth",
              "active_sp_holders_pending_sp_reward",
              "posting_rewards_scr",
              "last_account_update",
              "last_account_recovery",
              "name",
              "voting_power",
              "last_active_proved",
              "last_bandwidth_update",
              "active_sp_holders_cashout_time",
              "average_bandwidth",
              "last_market_bandwidth_update",
              "last_vote_time",
              "created_by_genesis",)

    for field in fields:
        assert field in data[0], "Required field is not in the response '%s'" % field
