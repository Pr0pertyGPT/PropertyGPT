pragma solidity 0.8.0;

contract VulnerableStaking {mapping(address => uint256) public balances;
uint256 public totalSupply;

function withdraw(uint256) public  {}

rule ValidateWithdrawEffects() {
    address $sender;
    uint256 $amount;
    uint256 balancesSenderBefore = balances[$sender];
    uint256 totalSupplyBefore = totalSupply;

    withdraw($amount);

    assert(balances[$sender] == balancesSenderBefore - $amount);
    assert(totalSupply == totalSupplyBefore - $amount);
}}