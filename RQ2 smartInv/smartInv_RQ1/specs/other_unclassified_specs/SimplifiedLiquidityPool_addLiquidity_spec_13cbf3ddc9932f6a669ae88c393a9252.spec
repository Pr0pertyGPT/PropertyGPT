pragma solidity 0.8.0;

contract SimplifiedLiquidityPool {mapping(address => mapping(address => uint256)) public liquidityBalance;

function addLiquidity(address,uint256) public  {}

rule LiquidityBalanceNotAffectedForNonParticipants() {
    address $token;
    address $provider; 
    uint256 $amount;
    address $other;
    
    require($other != $provider);

    uint256 balanceBefore = liquidityBalance[$token][$other];
    addLiquidity($token, $amount);
    uint256 balanceAfter = liquidityBalance[$token][$other];

    assert(balanceBefore == balanceAfter);
}}