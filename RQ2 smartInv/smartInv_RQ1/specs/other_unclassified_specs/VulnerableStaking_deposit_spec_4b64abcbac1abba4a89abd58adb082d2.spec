pragma solidity 0.8.0;

contract VulnerableStaking {mapping(address => uint256) public balances;
uint256 public totalSupply;

function deposit(uint256) public  {}

rule depositDoesNotAlterTotalSupplyIncorrectly() {
    uint256 $amount;
    uint256 totalSupplyBefore = totalSupply;
    address $sender = msg.sender;
    uint256 balanceBefore = balances[$sender];

    deposit($amount);

    assert(totalSupply == totalSupplyBefore + $amount);
    assert(balances[$sender] == balanceBefore + $amount);
}}