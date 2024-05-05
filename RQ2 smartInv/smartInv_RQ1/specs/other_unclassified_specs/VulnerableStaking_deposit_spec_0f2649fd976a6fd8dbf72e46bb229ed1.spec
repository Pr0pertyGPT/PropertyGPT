pragma solidity 0.8.0;

contract VulnerableStaking {mapping(address => uint256) public balances;
uint256 public totalSupply;

function deposit(uint256) public  {}

rule BalancedDepositIncreasesTotalSupply() {
    uint256 $depositAmount;
    address $depositor;
    uint256 balancesBefore = balances[$depositor];
    uint256 totalSupplyBefore = totalSupply;
    
    deposit($depositAmount);

    assert(balances[$depositor] == (balancesBefore + $depositAmount));
    assert(totalSupply == (totalSupplyBefore + $depositAmount));
}}