pragma solidity 0.8.0;

contract VulnerableTokenSwap {mapping(address => TokenPair) public tokenPairs;
mapping(address => mapping(address => uint)) public balances;
struct TokenPair {
        address token1;
        address token2;
    }

function deposit(address,uint256) public  {}

rule VerifyDepositEffects() {
    address $token;
    uint $amount;
    uint $init_balance_sender_token;
    uint $init_balance_sender_eth;

    balances[msg.sender][$token] = $init_balance_sender_token;
    balances[msg.sender][address(0)] = $init_balance_sender_eth; // Assuming address(0) represents ETH for simplification

    uint balanceBeforeSenderToken = balances[msg.sender][$token];
    uint balanceBeforeSenderEth = balances[msg.sender][address(0)];

    deposit($token, $amount);

    assert(balances[msg.sender][$token] == balanceBeforeSenderToken + $amount);
    assert(balances[msg.sender][address(0)] == balanceBeforeSenderEth);
}}