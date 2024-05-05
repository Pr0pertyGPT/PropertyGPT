pragma solidity 0.8.0;

contract VulnerableTokenSwap {mapping(address => TokenPair) public tokenPairs;
mapping(address => mapping(address => uint)) public balances;
struct TokenPair {
        address token1;
        address token2;
    }

function deposit(address,uint256) public  {}

rule BalanceIncreaseAfterDeposit() {
    address $token;
    uint256 $amount;
    uint256 initBalance = balances[msg.sender][$token];
    deposit($token, $amount);
    assert(balances[msg.sender][$token] == initBalance + $amount);
}}