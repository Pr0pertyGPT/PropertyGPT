pragma solidity 0.8.0;

contract VulnerableReserve {mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;

function donateToReserves(uint256) public  {}

rule DonateReservesPreconditions() {
    uint256 $amount;
    uint256 $init_balance;
    balances[msg.sender] = $init_balance;

    if ($amount <= $init_balance) {
        uint256 balanceBefore = balances[msg.sender];
        uint256 totalReserveBefore = totalReserve;
        donateToReserves($amount);
        
        assert(balanceBefore - $amount == balances[msg.sender]);
        assert(totalReserveBefore + $amount == totalReserve);
    } else {
        assert(false); // precondition not met, cannot execute donateToReserves as intended
    }
}}