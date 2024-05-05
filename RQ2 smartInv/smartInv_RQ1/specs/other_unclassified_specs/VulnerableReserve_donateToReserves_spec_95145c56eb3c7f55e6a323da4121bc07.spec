pragma solidity 0.8.0;

contract VulnerableReserve {mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;

function donateToReserves(uint256) public  {}

rule DonationIncreasesTotalReserveCorrectly() {
    address $donor;
    uint256 $init_balance;
    uint256 $amount;
    uint256 totalReserveBefore = totalReserve;

    balances[$donor] = $init_balance;

    require($amount <= $init_balance, "Amount less than initial balance for correctness");

    donateToReserves($amount);

    assert(totalReserve == totalReserveBefore + $amount);
}}