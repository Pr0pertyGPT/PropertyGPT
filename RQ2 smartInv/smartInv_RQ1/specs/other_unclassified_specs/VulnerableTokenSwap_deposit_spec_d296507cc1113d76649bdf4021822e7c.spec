pragma solidity 0.8.0;

contract VulnerableTokenSwap {mapping(address => TokenPair) public tokenPairs;
mapping(address => mapping(address => uint)) public balances;
struct TokenPair {
        address token1;
        address token2;
    }

function deposit(address,uint256) public  {}

rule CorrectDepositEffect() {
    address $token;
    uint256 $amount;
    address $sender = msg.sender;

    uint256 balanceBefore = balances[$sender][$token];
    deposit($token, $amount);

    // Verifying that the balance after deposit is correctly updated
    assert(balances[$sender][$token] == (balanceBefore + $amount));
}}