%lang starknet

from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.bool import TRUE
from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.math import assert_lt_felt, assert_not_zero
from starkware.cairo.common.uint256 import Uint256, uint256_check, uint256_le
from starkware.starknet.common.messages import send_message_to_l1
from starkware.starknet.common.syscalls import get_caller_address, get_contract_address

from contracts.l2.lib.wad_ray_math import (
    Wad,
    wad_sub,
    wad_to_ray,
    ray_mul_no_rounding,
    wad_le,
    wad_mul,
)
from contracts.l2.interfaces.IERC20 import IERC20
from contracts.l2.interfaces.Istatic_a_token import Istatic_a_token

const BRIDGE_REWARD_MESSAGE = 1;
const WITHDRAW_MESSAGE = 2;
const ETH_ADDRESS_BOUND = 2 ** 160;

// Storage.

@storage_var
func governor() -> (res: felt) {
}

@storage_var
func l1_bridge() -> (res: felt) {
}

@storage_var
func l2_token_to_l1_token(l2_token: felt) -> (l1_token: felt) {
}

@storage_var
func rewAAVE() -> (address: felt) {
}

// Events.

@event
func withdraw_initiated(
    l2_token: felt,
    l1_recipient: felt,
    amount: Uint256,
    caller: felt,
    current_rewards_index: Uint256,
) {
}

@event
func deposit_handled(
    l2_token: felt,
    l1_sender: felt,
    account: felt,
    amount: Uint256,
    block_number: Uint256,
    l1_rewards_index: Uint256,
) {
}

@event
func minted_rewards(l2_reward_token: felt, account: felt, amount: Uint256) {
}

@event
func bridged_rewards(caller: felt, l1_recipient: felt, amount: Uint256) {
}

@event
func rewards_index_updated(
    l2_token: felt, l1_sender: felt, block_number: Uint256, l1_rewards_index: Wad
) {
}

@event
func reward_token_updated(reward_token: felt) {
}

@event
func l1_bridge_updated(l1_bridge_address: felt) {
}

@event
func bridge_initialized(governor_address: felt) {
}

@event
func bridge_approved(l2_token: felt, l1_token: felt) {
}

// Getters.

// @notice Returns the governor of the contract
// @return Governor address
@view
func get_governor{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (
    res: felt
) {
    let (res) = governor.read();
    return (res,);
}

// @notice Returns the address of L1 bridge
// @return Address of the L1 bridge
@view
func get_l1_bridge{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (
    res: felt
) {
    let (res) = l1_bridge.read();
    return (res,);
}

// Internals

// @notice Asserts whether an L2 token has been approved by the bridge
// @param l2_token Address of the L2 token
func is_valid_l1_token{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    l2_token: felt
) {
    let (l1_token) = l2_token_to_l1_token.read(l2_token);
    with_attr error_message("No l1 token found for {l2_token}") {
        assert_not_zero(l1_token);
    }
    return ();
}

// @notice Asserts whether the caller of the function is the governor
func only_governor{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() {
    let (caller_address) = get_caller_address();
    let (governor_) = get_governor();
    with_attr error_message("Caller address should be {governor_}") {
        assert caller_address = governor_;
    }
    return ();
}

// @notice Asserts whether the caller of the function is L1 bridge
// @param from_address_ Caller address of an L1 handler function
func only_l1_bridge{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    from_address_: felt
) {
    let (expected_from_address) = get_l1_bridge();
    with_attr error_message("Expected deposit from l1_bridge: {expected_from_address}") {
        assert from_address_ = expected_from_address;
    }
    return ();
}

// @notice Asserts whether an address is valid Ethereum address
// @param l1_address L1 address to check
func only_valid_l1_address{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    l1_address: felt
) {
    with_attr error_message(
            "L1 address is not valid: it should be between 1 and 2 ** 160. Current value: {l1_address}") {
        assert_not_zero(l1_address);
        assert_lt_felt(l1_address, ETH_ADDRESS_BOUND);
    }
    return ();
}

// @notice Asserts whether the current contract is the owner of a token
// @param token_address Address of the token to check
func only_owned_token{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    token_address: felt
) {
    with_attr error_message("Bridge contract should be owner of the token.") {
        let (contract_address) = get_contract_address();
        let (token_owner) = IERC20.owner(token_address);
        assert token_owner = contract_address;
    }
    return ();
}

// Externals

// @notice Initializes the bridge by setting the governor address
// @param governor_address Address of the future governor of the bridge
@external
func initialize_bridge{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    governor_address: felt
) {
    let (governor_) = governor.read();
    with_attr error_message("Bridge already initialized") {
        assert governor_ = 0;
    }
    assert_not_zero(governor_address);
    governor.write(value=governor_address);
    bridge_initialized.emit(governor_address);
    return ();
}

// @notice Sets the address of L1 bridge
// @param l1_bridge_address Address of L1 bridge
@external
func set_l1_bridge{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    l1_bridge_address: felt
) {
    only_governor();
    // Check new address is valid.
    only_valid_l1_address(l1_bridge_address);

    // Set new value.
    l1_bridge.write(value=l1_bridge_address);

    l1_bridge_updated.emit(l1_bridge_address);
    return ();
}

// @notice Sets the address of the reward token
// @param reward_token Address of the reward token
@external
func set_reward_token{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    reward_token: felt
) {
    only_owned_token(reward_token);

    with_attr error_message("Reward token address should be non zero.") {
        assert_not_zero(reward_token);
    }

    only_governor();

    rewAAVE.write(reward_token);

    reward_token_updated.emit(reward_token);

    return ();
}

// @notice Adds a pair (L1 token, L2 token) to the bridge's mapping
// @param l1_token Address of the L1 token
// @param l2_token Address of the L2 token
@external
func approve_bridge{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    l1_token: felt, l2_token: felt
) {
    // the call is restricted to the governor.
    only_governor();

    // verify that the l2 token address was provided
    assert_not_zero(l2_token);

    let (l1_token_) = l2_token_to_l1_token.read(l2_token);
    with_attr error_message("L2 to L1 Bridge already setup") {
        assert l1_token_ = 0;
    }

    only_valid_l1_address(l1_token);

    l2_token_to_l1_token.write(l2_token, l1_token);
    bridge_approved.emit(l2_token, l1_token);
    return ();
}

// @notice Initiates withdrawal of static aTokens from L2 to L1 by burning L2 tokens and sending a message to L1
// @param l2_token Address of the L2 token (static aToken)
// @param l1_recipient Address of the L1 recipient of this withdrawal
// @param amount Amount of L2 token to be withdrawn from L2 to L1
@external
func initiate_withdraw{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    l2_token: felt, l1_recipient: felt, amount: Uint256, to_underlying_asset: felt
) {
    assert_not_zero(l2_token);

    let (to_address) = get_l1_bridge();

    // check l1 address is valid.
    only_valid_l1_address(l1_recipient);

    let (l1_token) = l2_token_to_l1_token.read(l2_token);
    with_attr error_message("No l1 token found for {l2_token}") {
        assert_not_zero(l1_token);
    }

    let (current_rewards_index) = Istatic_a_token.get_rewards_index(contract_address=l2_token);

    // call burn on l2_token contract.
    let (caller_address) = get_caller_address();

    // check input
    with_attr error_message("incorrect flag: value should be either 0 or 1") {
        assert to_underlying_asset * to_underlying_asset = to_underlying_asset;
    }

    // prepare l1 message
    let (message_payload: felt*) = alloc();
    assert message_payload[0] = WITHDRAW_MESSAGE;
    assert message_payload[1] = l1_token;
    assert message_payload[2] = caller_address;
    assert message_payload[3] = l1_recipient;
    assert message_payload[4] = amount.low;
    assert message_payload[5] = amount.high;
    assert message_payload[6] = current_rewards_index.wad.low;
    assert message_payload[7] = current_rewards_index.wad.high;
    assert message_payload[8] = to_underlying_asset;

    // burn static_a_tokens
    IERC20.burn(contract_address=l2_token, account=caller_address, amount=amount);

    // send witdraw message to l1
    send_message_to_l1(to_address=to_address, payload_size=9, payload=message_payload);

    withdraw_initiated.emit(
        l2_token, l1_recipient, amount, caller_address, current_rewards_index.wad
    );
    return ();
}

// @notice Initiates withdrawal of reward tokens from L2 to L1 by burning L2 tokens and sending a message to L1
// @param l1_recipient Address of the L1 recipient of this withdrawal
// @param amount Amount of reward tokens to be withdrawn from L2 to L1
@external
func bridge_rewards{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    l1_recipient: felt, amount: Uint256
) {
    only_valid_l1_address(l1_recipient);

    let (to_address) = get_l1_bridge();

    let (token_owner) = get_caller_address();

    let (reward_token) = rewAAVE.read();

    // prepare l1 message for bridging tokens
    let (message_payload: felt*) = alloc();
    assert message_payload[0] = BRIDGE_REWARD_MESSAGE;
    assert message_payload[1] = token_owner;
    assert message_payload[2] = l1_recipient;
    assert message_payload[3] = amount.low;
    assert message_payload[4] = amount.high;

    // burn rewards
    IERC20.burn(contract_address=reward_token, account=token_owner, amount=amount);

    // send message to l1
    send_message_to_l1(to_address=to_address, payload_size=5, payload=message_payload);

    bridged_rewards.emit(token_owner, l1_recipient, amount);

    return ();
}

// @notice Handler called when L1 bridge deposit function is called. Function that mints L2 static aTokens and updates its state (latest L1 update block number and L1 rewards index).
// @param from_address L1 caller address of this function
// @param l1_sender L1 caller address of L1 bridge deposit function
// @param l2_recipient L2 address of bridged tokens' recipient
// @param l2_token L2 address of the token
// @param amount_low Amount of L2 token to be sent (low part i.e. first 128 bits of an uint256)
// @param amount_high Amount of L2 token to be sent (high part i.e. last 128 bits of an uint256)
// @param block_number_low L1 block number (low part)
// @param block_number_high L1 block number (high part)
// @param l1_rewards_index_low L1 rewards index (low part)
// @param l1_rewards_index_high L1 rewards index (high part)
@l1_handler
func handle_deposit{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    from_address: felt,
    l1_sender: felt,
    l2_recipient: felt,
    l2_token: felt,
    amount_low: felt,
    amount_high: felt,
    block_number_low: felt,
    block_number_high: felt,
    l1_rewards_index_low: felt,
    l1_rewards_index_high: felt,
) {
    alloc_locals;
    only_l1_bridge(from_address_=from_address);

    let amount_ = Uint256(low=amount_low, high=amount_high);
    local amount: Wad = Wad(amount_);

    let l1_rewards_index_ = Uint256(low=l1_rewards_index_low, high=l1_rewards_index_high);
    local l1_rewards_index: Wad = Wad(l1_rewards_index_);

    let block_number = Uint256(low=block_number_low, high=block_number_high);

    with_attr error_message("High or low overflows 128 bit bound {amount_}") {
        uint256_check(amount_);
    }

    with_attr error_message("High or low overflows 128 bit bound {l1_rewards_index_}") {
        uint256_check(l1_rewards_index_);
    }

    with_attr error_message("High or low overflows 128 bit bound {block_number}") {
        uint256_check(block_number);
    }

    assert_not_zero(l2_token);

    let (reward_token) = rewAAVE.read();

    // handle the difference of the index at send and receive
    let (current_index) = Istatic_a_token.get_rewards_index(l2_token);
    let (le) = wad_le(current_index, l1_rewards_index);
    if (le == TRUE) {
        Istatic_a_token.push_rewards_index(
            contract_address=l2_token, block_number=block_number, rewards_index=l1_rewards_index
        );
    } else {
        let (reward_diff) = wad_sub(current_index, l1_rewards_index);
        let (reward_outstanding) = wad_mul(reward_diff, amount);
        IERC20.mint(reward_token, l2_recipient, reward_outstanding.wad);
    }

    // Call mint on l2_token contract.
    IERC20.mint(l2_token, l2_recipient, amount.wad);
    deposit_handled.emit(
        l2_token, l1_sender, l2_recipient, amount.wad, block_number, l1_rewards_index.wad
    );
    return ();
}

// @notice Mints rewards tokens to a given L2 recipient. Function is called by a static aToken contract.
// @param recipient L2 address of tokens' recipient
// @param amount Amount of reward tokens to be minted
@external
func mint_rewards{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    recipient: felt, amount: Uint256
) {
    // get the address of the ETHStaticAToken
    let (l2_token) = get_caller_address();
    // check if l1 token exists
    is_valid_l1_token(l2_token);
    let (reward_token) = rewAAVE.read();
    // mints rewAAVE for user
    IERC20.mint(reward_token, recipient, amount);
    minted_rewards.emit(reward_token, recipient, amount);
    return ();
}

// @notice Handler called when L1 bridge updateL2State function is called. Function that updates the state (latest L1 update block number and L1 rewards index) of a given static aToken.
// @param from_address L1 caller address of this function
// @param l1_sender L1 caller address of L1 bridge deposit function
// @param l2_token L2 address of the token
// @param block_number_low L1 block number (low part)
// @param block_number_high L1 block number (high part)
// @param l1_rewards_index_low L1 rewards index (low part)
// @param l1_rewards_index_high L1 rewards index (high part)
@l1_handler
func handle_index_update{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    from_address: felt,
    l1_sender: felt,
    l2_token: felt,
    block_number_low: felt,
    block_number_high: felt,
    l1_rewards_index_low: felt,
    l1_rewards_index_high: felt,
) {
    alloc_locals;
    only_l1_bridge(from_address_=from_address);

    let l1_rewards_index_ = Uint256(low=l1_rewards_index_low, high=l1_rewards_index_high);
    local l1_rewards_index: Wad = Wad(l1_rewards_index_);

    let block_number = Uint256(low=block_number_low, high=block_number_high);

    with_attr error_message("High or low overflows 128 bit bound {l1_rewards_index_}") {
        uint256_check(l1_rewards_index_);
    }

    with_attr error_message("High or low overflows 128 bit bound {block_number}") {
        uint256_check(block_number);
    }

    assert_not_zero(l2_token);

    Istatic_a_token.push_rewards_index(
        contract_address=l2_token, block_number=block_number, rewards_index=l1_rewards_index
    );
    rewards_index_updated.emit(l2_token, l1_sender, block_number, l1_rewards_index);
    return ();
}
