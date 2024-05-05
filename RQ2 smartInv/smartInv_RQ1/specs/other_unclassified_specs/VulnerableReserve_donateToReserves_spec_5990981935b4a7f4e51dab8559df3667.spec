pragma solidity 0.8.0;

contract VulnerableReserve {mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;

function donateToReserves(uint256) public  {}

rule DonorBalanceDecreasesOnDonation() {
    address $donor;
    uint256 $donationAmount;
    uint256 balanceBefore = balances[$donor];
    uint256 totalReserveBefore = totalReserve;

    donateToReserves($donationAmount);

    assert(balances[$donor] == balanceBefore - $donationAmount);
    assert(totalReserve == totalReserveBefore + $donationAmount);
}}