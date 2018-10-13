from enum import Enum


class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__) if len(cls.__members__) else 0
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class Operations(AutoNumber):
    vote_operation = ()
    comment_operation = ()
    transfer_operation = ()
    transfer_to_scorumpower_operation = ()
    withdraw_scorumpower_operation = ()
    account_create_by_committee_operation = ()
    account_create_operation = ()
    account_create_with_delegation_operation = ()
    account_update_operation = ()
    witness_update_operation = ()
    account_witness_vote_operation = ()
    account_witness_proxy_operation = ()
    delete_comment_operation = ()
    comment_options_operation = ()
    set_withdraw_scorumpower_route_to_account_operation = ()
    set_withdraw_scorumpower_route_to_dev_pool_operation = ()
    prove_authority_operation = ()
    request_account_recovery_operation = ()
    recover_account_operation = ()
    change_recovery_account_operation = ()
    escrow_approve_operation = ()
    escrow_dispute_operation = ()
    escrow_release_operation = ()
    escrow_transfer_operation = ()
    decline_voting_rights_operation = ()
    delegate_scorumpower_operation = ()
    create_budget_operation = ()
    close_budget_operation = ()
    proposal_vote_operation = ()
    proposal_create_operation = ()
    atomicswap_initiate_operation = ()
    atomicswap_redeem_operation = ()
    atomicswap_refund_operation = ()
    close_budget_by_advertising_moderator_operation = ()
    update_budget_operation = ()
    # virtual operations
    author_reward_operation = ()
    comment_benefactor_reward_operation = ()
    comment_payout_update_operation = ()
    comment_reward_operation = ()
    curation_reward_operation = ()
    hardfork_operation = ()
    producer_reward_operation = ()
    active_sp_holders_reward_operation = ()
    return_scorumpower_delegation_operation = ()
    shutdown_witness_operation = ()
    witness_miss_block_operation = ()
    expired_contract_refund_operation = ()
    acc_finished_vesting_withdraw_operation = ()
    devpool_finished_vesting_withdraw_operation = ()
    acc_to_acc_vesting_withdraw_operation = ()
    devpool_to_acc_vesting_withdraw_operation = ()
    acc_to_devpool_vesting_withdraw_operation = ()
    devpool_to_devpool_vesting_withdraw_operation = ()
    proposal_virtual_operation = ()
    allocate_cash_from_advertising_budget_operation = ()
    cash_back_from_advertising_budget_to_owner_operation = ()

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value


def test_serialize():
    x = Operations.transfer_operation

    assert x.value == 2
    assert x.name == "transfer_operation"

    assert int(x) == 2
    assert str(x) == "transfer_operation"


def test_string_to_operation():
    assert Operations['transfer_operation'] == Operations.transfer_operation
