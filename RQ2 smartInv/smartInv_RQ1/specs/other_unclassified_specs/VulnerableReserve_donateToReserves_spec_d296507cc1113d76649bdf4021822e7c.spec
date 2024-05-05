pragma solidity 0.8.0;

contract VulnerableReserve {mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;

function donateToReserves(uint256) public  {}

rule DonateReservesBalanceConsistency() {
    uint256 $donationAmount;
    address $donor;
    uint256 init_balance = balances[$donor];
    uint256 totalReserveBefore = totalReserve;

    require(balances[$donor] >= $donationAmount);

    donateToReserves($donationAmount);

    assert(balances[$donor] == init_balance - $donationAmount);
    assert(totalReserve == totalReserveBefore + $donationAmount);
}}