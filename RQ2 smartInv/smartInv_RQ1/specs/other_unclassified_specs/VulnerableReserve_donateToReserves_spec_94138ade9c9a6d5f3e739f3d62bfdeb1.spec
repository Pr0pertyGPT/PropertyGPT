pragma solidity 0.8.0;

contract VulnerableReserve {mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;

function donateToReserves(uint256) public  {}

rule CorrectReserveDonation() {
    address $donor;
    uint256 $donationAmount;
    uint256 donorBalanceBefore = balances[$donor];
    uint256 totalReserveBefore = totalReserve;
    donateToReserves($donationAmount);

    if (balances[$donor] == donorBalanceBefore - $donationAmount) {
        assert(totalReserve == totalReserveBefore + $donationAmount);
    } else {
        assert(balances[$donor] == donorBalanceBefore);
    }
}}