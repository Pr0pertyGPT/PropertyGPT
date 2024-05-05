pragma solidity 0.8.0;

contract VulnerableReserve {mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;

function deposit(uint256) public  {}

rule DepositIncreasesBalanceCorrectly() {
    address $account;
    uint256 $depositAmount;
    uint256 balanceBefore = balances[$account];
    deposit($depositAmount);

    assert(balanceBefore + $depositAmount == balances[$account]);
}}