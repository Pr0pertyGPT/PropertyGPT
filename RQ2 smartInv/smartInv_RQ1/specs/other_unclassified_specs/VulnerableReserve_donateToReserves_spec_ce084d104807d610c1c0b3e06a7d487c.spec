pragma solidity 0.8.0;

contract VulnerableReserve {mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;

function donateToReserves(uint256) public  {}

rule DonateDoesNotAlterOtherBalances() {
    address $donor;
    uint256 $donateAmount;
    address $other;
    uint256 $otherInitialBalance = balances[$other];

    require($other != $donor);

    donateToReserves($donateAmount);
    assert(balances[$other] == $otherInitialBalance);
}}