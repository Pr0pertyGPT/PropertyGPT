pragma solidity 0.8.0;

contract VulnerableReserve {mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;

function donateToReserves(uint256) public  {}

rule DonateDoesNotAlterOtherBalances() {
    address $donor;
    uint256 $donationAmount;
    address $other;
    uint256 $otherInitialBalance;

    balances[$other] = $otherInitialBalance;

    require($other != $donor);

    uint256 balanceBeforeDonation = balances[$other];
    donateToReserves($donationAmount);
    assert(balanceBeforeDonation == balances[$other]);
}}