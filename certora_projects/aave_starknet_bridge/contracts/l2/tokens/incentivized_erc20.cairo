%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.uint256 import Uint256, uint256_add, uint256_sub, uint256_le
from starkware.starknet.common.syscalls import get_caller_address
from starkware.cairo.common.bool import TRUE, FALSE
from starkware.cairo.common.math import assert_not_zero
from contracts.l2.lib.wad_ray_math import (
    Wad,
    wad_to_ray,
    wad_add,
    Ray,
    ray_add,
    ray_sub,
    ray_mul_no_rounding,
    ray_to_wad,
    ray_to_wad_no_rounding,
)
from contracts.l2.dependencies.openzeppelin.token.erc20.library import ERC20

@storage_var
func l2_bridge() -> (address: felt) {
}

@storage_var
func last_update() -> (block_number: Uint256) {
}

@storage_var
func rewards_index() -> (res: Wad) {
}

// user => rewards index at last interaction (in WADs)
@storage_var
func user_snapshot_rewards_index(user: felt) -> (rewards_index: Wad) {
}

// user => unclaimed_rewards (in WADs)
@storage_var
func unclaimed_rewards(user: felt) -> (unclaimed: Wad) {
}

// @notice Updates rewards index value for a given user.
// @param user Address of the user
func update_user_snapshot_rewards_index{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}(user: felt) {
    let (rewards_index_) = rewards_index.read();
    user_snapshot_rewards_index.write(user, rewards_index_);
    return ();
}

// @notice Updates unclaimed amount of rewards and rewards index value for a given user.
// @param user Address of the user
func update_user{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(user: felt) {
    alloc_locals;
    let (balance) = ERC20.balance_of(user);
    if (balance.high + balance.low == 0) {
        update_user_snapshot_rewards_index(user);
    } else {
        let (pending) = incentivized_erc20_get_pending_rewards(user);
        let (unclaimed) = incentivized_erc20_get_user_unclaimed_rewards(user);
        let (unclaimed, overflow) = wad_add(unclaimed, pending);
        assert overflow = FALSE;
        unclaimed_rewards.write(user, unclaimed);
        update_user_snapshot_rewards_index(user);
    }
    return ();
}

// @notice Updates unclaimed amount of rewards and rewards index value for users involved in a transfer.
// @param from_ Address of the sender
// @param to Address of the recipient
func incentivized_erc20_before_token_transfer{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}(from_: felt, to: felt) {
    alloc_locals;
    if (from_ == 0) {
        // do nothing
        tempvar syscall_ptr = syscall_ptr;
        tempvar pedersen_ptr = pedersen_ptr;
        tempvar range_check_ptr = range_check_ptr;
    } else {
        update_user(from_);
        tempvar syscall_ptr = syscall_ptr;
        tempvar pedersen_ptr = pedersen_ptr;
        tempvar range_check_ptr = range_check_ptr;
    }
    if (to == 0) {
        // do nothing
    } else {
        update_user(to);
    }
    return ();
}

// @notice Computes the pending amount of rewards for a given user.
// @param user Address of the user
// @return Amount of pending rewards in Wad
func incentivized_erc20_get_pending_rewards{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}(user: felt) -> (pending_rewards: Wad) {
    alloc_locals;
    let (balance) = ERC20.balance_of(user);
    let (balance_in_ray) = wad_to_ray(Wad(balance));
    let (rewards_index_) = rewards_index.read();
    let (user_snapshot_rewards_index_) = user_snapshot_rewards_index.read(user);
    let (user_snapshot_rewards_index_ray) = wad_to_ray(user_snapshot_rewards_index_);
    let (rewards_index_ray) = wad_to_ray(rewards_index_);
    let (rewards_index_since_last_interaction) = ray_sub(
        rewards_index_ray, user_snapshot_rewards_index_ray
    );
    let (pending_rewards) = ray_mul_no_rounding(
        rewards_index_since_last_interaction, balance_in_ray
    );
    let (pending_) = ray_to_wad_no_rounding(pending_rewards);
    return (pending_,);
}

// @notice Returns the amount of rewards a user can claim.
// @param user Address of the user
// @return Amount of claimable rewards in Wad
func incentivized_erc20_get_claimable_rewards{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}(user: felt) -> (incentivized_erc20_rewards: Wad) {
    alloc_locals;
    let (unclaimed_rewards_) = unclaimed_rewards.read(user);
    let (pending) = incentivized_erc20_get_pending_rewards(user);
    let (incentivized_erc20_rewards, overflow) = wad_add(unclaimed_rewards_, pending);
    assert overflow = FALSE;

    return (incentivized_erc20_rewards,);
}

// @notice Returns the amount of rewards claimed by a user, and sets his amount of claimable rewards to zero.
// @param user Address of the user
// @return Amount of claimed rewards in Wad
func incentivized_erc20_claim_rewards{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}(user: felt) -> (rewards: Wad) {
    alloc_locals;
    let (rewards) = incentivized_erc20_get_claimable_rewards(user);

    unclaimed_rewards.write(user, Wad(Uint256(0, 0)));

    if (rewards.wad.high + rewards.wad.low == 0) {
        return (Wad(Uint256(0, 0)),);
    } else {
        update_user_snapshot_rewards_index(user);
        return (rewards,);
    }
}

// @notice Updates token's state with last block number and rewards index.
// @param block_number L1 block number
// @param new_rewards_index L1 rewards index in Wad
func incentivized_erc20_push_rewards_index{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}(block_number: Uint256, new_rewards_index: Wad) {
    alloc_locals;
    incentivized_erc20_only_bridge();
    let (last_block_number) = last_update.read();
    // This is le because the rewards may update in a block
    let (le) = uint256_le(last_block_number, block_number);
    if (le == TRUE) {
        let (prev_index) = rewards_index.read();
        let (le) = uint256_le(prev_index.wad, new_rewards_index.wad);
        if (le == TRUE) {
            last_update.write(block_number);
            rewards_index.write(new_rewards_index);
            return ();
        } else {
            return ();
        }
    } else {
        return ();
    }
}

// @notice Returns the rewards index stored at last interaction.
// @return Rewards index in Wad
func incentivized_erc20_get_rewards_index{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}() -> (res: Wad) {
    return rewards_index.read();
}

// @notice Returns the rewards index stored at last interaction for a given user.
// @param user Address of a user
// @return Rewards index in Wad
func incentivized_erc20_get_user_rewards_index{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}(user: felt) -> (res: Wad) {
    let (res) = user_snapshot_rewards_index.read(user);
    return (res,);
}

// @notice Returns the amount of rewards not claimed yet for a given user.
// @param user Address of a user
// @return Amount of rewards not claimed yet in Wad
func incentivized_erc20_get_user_unclaimed_rewards{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}(user: felt) -> (res: Wad) {
    let (res) = unclaimed_rewards.read(user);
    return (res,);
}

// @notice Returns the block number stored at last interaction.
// @return Block number
func incentivized_erc20_get_last_update{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}() -> (block_number: Uint256) {
    return last_update.read();
}

// @notice Sets the address of L2 bridge
// @param l2_bridge_ Address of the L2 bridge
func incentivized_erc20_set_l2_bridge{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}(l2_bridge_: felt) {
    with_attr error_message("L2 bridge address should be non zero.") {
        assert_not_zero(l2_bridge_);
    }
    l2_bridge.write(l2_bridge_);
    return ();
}

// @notice Returns the address of L2 bridge
// @return Address of the L2 bridge
func incentivized_erc20_get_l2_bridge{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}() -> (l2_bridge_: felt) {
    let (l2_bridge_) = l2_bridge.read();
    return (l2_bridge_,);
}

// @notice Asserts whether the caller address if L2 bridge.
func incentivized_erc20_only_bridge{
    syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr
}() {
    let (caller_address) = get_caller_address();
    let (l2_bridge_) = l2_bridge.read();
    with_attr error_message("Caller address should be bridge: {l2_bridge_}") {
        assert caller_address = l2_bridge_;
    }
    return ();
}
