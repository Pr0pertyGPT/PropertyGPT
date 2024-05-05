pragma solidity 0.8.0;

contract VulnerableTokenSwap {mapping(address => TokenPair) public tokenPairs;
mapping(address => mapping(address => uint)) public balances;
struct TokenPair {
        address token1;
        address token2;
    }

function deposit(address,uint256) public  {}

rule depositEnsuresCorrectBalanceUpdate() {
    address $token;
    uint256 $amount;
    address $sender = msg.sender;
    
    uint256 senderTokenBalanceBefore = balances[$sender][$token];
    
    deposit($token, $amount);

    assert(balances[$sender][$token] == senderTokenBalanceBefore + $amount);
}}