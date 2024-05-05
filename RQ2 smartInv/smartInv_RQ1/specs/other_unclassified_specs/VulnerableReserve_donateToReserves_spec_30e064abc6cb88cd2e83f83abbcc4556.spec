pragma solidity 0.8.0;

contract VulnerableReserve {mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;

function donateToReserves(uint256) public  {}

rule ValidateReserveDonationEffect() {
    uint256 $donationAmount;
    address $donor;
    uint256 initialDonorBalance = balances[$donor];
    uint256 initialReserveAmount = totalReserve;

    donateToReserves($donationAmount);

    assert(balances[$donor] == initialDonorBalance - $donationAmount);
    assert(totalReserve == initialReserveAmount + $donationAmount);
}}