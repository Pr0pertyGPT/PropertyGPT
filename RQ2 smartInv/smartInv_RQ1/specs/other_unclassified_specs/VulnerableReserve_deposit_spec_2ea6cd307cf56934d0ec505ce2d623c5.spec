pragma solidity 0.8.0;

contract VulnerableReserve {mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;

function deposit(uint256) public  {}

rule DepositIncreasesBalanceCorrectly() {
    address $sender;
    uint256 $depositAmount;
    uint256 balanceBefore = balances[$sender];
    deposit($depositAmount);

    assert(balances[$sender] == balanceBefore + $depositAmount);
}}