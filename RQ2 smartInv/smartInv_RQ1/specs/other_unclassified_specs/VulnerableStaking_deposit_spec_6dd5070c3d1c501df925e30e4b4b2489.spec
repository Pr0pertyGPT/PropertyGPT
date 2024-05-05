pragma solidity 0.8.0;

contract VulnerableStaking {mapping(address => uint256) public balances;
uint256 public totalSupply;

function withdraw(uint256) public  {}

rule CorrectBalanceUpdateOnWithdrawal() {
    address $account;
    uint256 $withdrawAmount;
    uint256 $balanceBefore = balances[$account];
    uint256 $totalSupplyBefore = totalSupply;

    withdraw($withdrawAmount);

    assert(balances[$account] == $balanceBefore - $withdrawAmount);
    assert(totalSupply == $totalSupplyBefore - $withdrawAmount);
}}