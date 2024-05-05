pragma solidity 0.8.0;

contract VulnerableReserve {mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;

function donateToReserves(uint256) public  {}

rule IntegrityOfDonateToReserves() {
    address $msgSender;
    uint256 $amount;
    uint256 balanceSenderBefore = balances[$msgSender];
    uint256 totalReserveBefore = totalReserve;
    donateToReserves($amount);

    assert(balances[$msgSender] == balanceSenderBefore - $amount);
    assert(totalReserve == totalReserveBefore + $amount);
}}