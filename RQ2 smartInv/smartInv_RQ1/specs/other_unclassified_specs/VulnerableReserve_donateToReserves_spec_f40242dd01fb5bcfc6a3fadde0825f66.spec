pragma solidity 0.8.0;

contract VulnerableReserve {mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;

function donateToReserves(uint256) public  {}

rule DonateToReservesMaintainsUserBalanceIntegrity() {
    address $user;
    uint256 $initial_balance;
    balances[$user] = $initial_balance; // Mimic initial setup for a user's balance
    uint256 $amount;

    require($initial_balance >= $amount, "Setting up for valid donation scenario");

    uint256 balanceBeforeDonation = balances[$user];
    uint256 totalReserveBeforeDonation = totalReserve;
    
    donateToReserves($amount);

    assert(balances[$user] == balanceBeforeDonation - $amount);
    assert(totalReserve == totalReserveBeforeDonation + $amount);
}}