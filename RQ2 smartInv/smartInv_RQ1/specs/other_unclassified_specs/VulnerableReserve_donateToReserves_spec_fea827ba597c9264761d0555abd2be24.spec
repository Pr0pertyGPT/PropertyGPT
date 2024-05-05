pragma solidity 0.8.0;

contract VulnerableReserve {mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;

function donateToReserves(uint256) public  {}

rule DonationPreservesTotalValue() {
    uint256 $init_balance;
    uint256 $amount;
    address $sender;

    balances[$sender] = $init_balance;
    uint256 totalReserveBefore = totalReserve;

    require(balances[$sender] >= $amount);
    donateToReserves($amount);

    assert(totalReserve == totalReserveBefore + $amount);
    assert(balances[$sender] == $init_balance - $amount);
}}