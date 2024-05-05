pragma solidity 0.8.0;

contract VulnerableStaking {mapping(address => uint256) public balances;
uint256 public totalSupply;

function deposit(uint256) public  {}

rule EnsureDepositIncreasesBalancesAndTotalSupply() {
    address sender;
    uint256 amount;
    uint256 initialBalance = balances[sender];
    uint256 initialTotalSupply = totalSupply;

    deposit(amount); // Adjusted to match expected argument count

    assert(balances[sender] == initialBalance + amount);
    assert(totalSupply == initialTotalSupply + amount);
}}