%lang starknet

from starkware.cairo.common.uint256 import Uint256
from contracts.l2.lib.wad_ray_math import Wad

@contract_interface
namespace Istatic_a_token {
    func name() -> (name: felt) {
    }

    func symbol() -> (symbol: felt) {
    }

    func totalSupply() -> (totalSupply: Uint256) {
    }

    func decimals() -> (decimals: felt) {
    }

    func balanceOf(account: felt) -> (balance: Uint256) {
    }

    func allowance(owner: felt, spender: felt) -> (remaining: Uint256) {
    }

    func transfer(recipient: felt, amount: Uint256) -> (success: felt) {
    }

    func transferFrom(sender: felt, recipient: felt, amount: Uint256) -> (success: felt) {
    }

    func approve(spender: felt, amount: Uint256) -> (success: felt) {
    }

    func increaseAllowance(spender: felt, added_value: Uint256) -> (success: felt) {
    }

    func decreaseAllowance(spender: felt, subtracted_value: Uint256) -> (success: felt) {
    }

    func mint(recipient: felt, amount: Uint256) {
    }

    func claim_rewards(recipient: felt) -> (claimed: Uint256) {
    }

    func increaseLifetimeRewards(amount: Uint256) {
    }

    func burn(account: felt, amount: Uint256) {
    }

    func push_rewards_index(block_number: Uint256, rewards_index: Wad) {
    }

    func initialize_static_a_token(
        name: felt,
        symbol: felt,
        decimals: felt,
        initial_supply: Uint256,
        recipient: felt,
        controller: felt,
    ) {
    }

    func get_rewards_index() -> (rewards_index: Wad) {
    }
}
