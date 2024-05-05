// SPDX-License-Identifier: MIT
// OpenZeppelin Cairo Contracts v0.1.0 (token/erc20/ERC20_Mintable.cairo)

%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.uint256 import Uint256
from starkware.cairo.common.bool import TRUE
from starkware.cairo.common.math import assert_not_zero

from contracts.l2.dependencies.openzeppelin.token.erc20.library import ERC20
from contracts.l2.dependencies.openzeppelin.access.ownable import Ownable
from contracts.l2.lib.version_initializable import VersionedInitializable

//
// Version
//

const REVISION = 1;

//
// Events
//

@event
func rewAAVE_initialized(
    name: felt, symbol: felt, decimals: felt, initial_supply: Uint256, recipient: felt, owner: felt
) {
}

//
// Constructor
//

// @notice Initializes reward token by providing name, symbol, decimals, an initial supply and its recipient, and the owner address
// @param name Token name
// @param symbol Token symbol
// @param decimals Number of decimals the token uses
// @param initial_supply Initial amount of token minted to a recipient
// @param recipient Address of the recipient who receives the initial supply
// @param owner Token owner address
@external
func initialize_rewAAVE{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    name: felt, symbol: felt, decimals: felt, initial_supply: Uint256, recipient: felt, owner: felt
) {
    VersionedInitializable.initializer(REVISION);

    // check inputs
    with_attr error_message("rewAAVE: name should be non zero") {
        assert_not_zero(name);
    }
    with_attr error_message("rewAAVE: symbol should be non zero") {
        assert_not_zero(symbol);
    }
    with_attr error_message("rewAAVE: decimals should be non zero") {
        assert_not_zero(decimals);
    }
    with_attr error_message("rewAAVE: owner address should be non zero") {
        assert_not_zero(owner);
    }

    ERC20.initializer(name, symbol, decimals);
    ERC20._mint(recipient, initial_supply);
    Ownable.initializer(owner);
    rewAAVE_initialized.emit(name, symbol, decimals, initial_supply, recipient, owner);
    return ();
}

//
// Getters
//

// @notice Returns the token name.
// @return The token name.
@view
func name{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (name: felt) {
    let (name) = ERC20.name();
    return (name,);
}

// @notice Returns the token symbol.
// @return The token symbol.
@view
func symbol{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (symbol: felt) {
    let (symbol) = ERC20.symbol();
    return (symbol,);
}

// @notice Returns the total supply of the token.
// @return The total supply.
@view
func totalSupply{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (
    totalSupply: Uint256
) {
    let (totalSupply: Uint256) = ERC20.total_supply();
    return (totalSupply,);
}

// @notice Returns the number of decimals the token uses.
// @return The number of decimals.
@view
func decimals{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (
    decimals: felt
) {
    let (decimals) = ERC20.decimals();
    return (decimals,);
}

// @notice Returns the balance of reward tokens for a given user
// @param account Address we want to know the balance
// @return Balance of tokens
@view
func balanceOf{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(account: felt) -> (
    balance: Uint256
) {
    let (balance: Uint256) = ERC20.balance_of(account);
    return (balance,);
}

// @notice Returns the amount which spender is allowed to withdraw from owner.
// @param owner Address of a token owner
// @param spender Address of a user
// @return Amount of tokens
@view
func allowance{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    owner: felt, spender: felt
) -> (remaining: Uint256) {
    let (remaining: Uint256) = ERC20.allowance(owner, spender);
    return (remaining,);
}

// @notice Returns the address of token owner.
// @return Address of token owner.
@view
func owner{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (owner: felt) {
    let (owner) = Ownable.owner();
    return (owner=owner);
}

//
// Externals
//

// @notice Transfers a given amount of tokens to a recipient.
// @param recipient Address of the recipient
// @param amount Amount of tokens to send
// @return Boolean TRUE
@external
func transfer{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    recipient: felt, amount: Uint256
) -> (success: felt) {
    ERC20.transfer(recipient, amount);
    return (TRUE,);
}

// @notice Transfers a given amount of tokens from a sender to a recipient.
// @param sender Address of the sender
// @param recipient Address of the recipient
// @param amount Amount of tokens to send
// @return Boolean TRUE
@external
func transferFrom{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    sender: felt, recipient: felt, amount: Uint256
) -> (success: felt) {
    ERC20.transfer_from(sender, recipient, amount);
    return (TRUE,);
}

// @notice Allows spender to withdraw from your account multiple times, up to a given amount.
// @param spender Address of the spender
// @param amount Amount of tokens to send
// @return Boolean TRUE
@external
func approve{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    spender: felt, amount: Uint256
) -> (success: felt) {
    ERC20.approve(spender, amount);
    return (TRUE,);
}

// @notice Increases the amount of tokens a spender can withdraw from your account.
// @param spender Address of the spender
// @param added_value Amount of tokens to add
// @return Boolean TRUE
@external
func increaseAllowance{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    spender: felt, added_value: Uint256
) -> (success: felt) {
    ERC20.increase_allowance(spender, added_value);
    return (TRUE,);
}

// @notice Decreases the amount of tokens a spender can withdraw from your account.
// @param spender Address of the spender
// @param subtracted_value Amount of tokens to substract
// @return Boolean TRUE
@external
func decreaseAllowance{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    spender: felt, subtracted_value: Uint256
) -> (success: felt) {
    ERC20.decrease_allowance(spender, subtracted_value);
    return (TRUE,);
}

// @notice Increases the token balance of a recipient by a given amount.
// @param recipient Address of the recipient
// @param amount Amount of tokens to add
@external
func mint{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    to: felt, amount: Uint256
) {
    Ownable.assert_only_owner();
    ERC20._mint(to, amount);
    return ();
}

// @notice Decreases the token balance of a user by a given amount.
// @param account Address of the user
// @param amount Amount of tokens to substract
@external
func burn{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(
    account: felt, amount: Uint256
) {
    alloc_locals;
    Ownable.assert_only_owner();
    ERC20._burn(account=account, amount=amount);
    return ();
}
