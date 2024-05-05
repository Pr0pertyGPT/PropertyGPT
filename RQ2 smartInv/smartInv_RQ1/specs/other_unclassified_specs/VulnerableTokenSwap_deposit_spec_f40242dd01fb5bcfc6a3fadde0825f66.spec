pragma solidity 0.8.0;

contract VulnerableTokenSwap {mapping(address => TokenPair) public tokenPairs;
mapping(address => mapping(address => uint)) public balances;
struct TokenPair {
        address token1;
        address token2;
    }

function deposit(address,uint256) public  {}

rule EnsureBalanceIncreaseOnDeposit() {
    address $token;
    address $user;
    uint256 $amount;
    uint256 balanceOfUserBefore = balances[$user][$token];
    uint256 balanceOfUserAfter;

    deposit($token, $amount);
    balanceOfUserAfter = balances[$user][$token];

    assert(balanceOfUserAfter == balanceOfUserBefore + $amount);
}}