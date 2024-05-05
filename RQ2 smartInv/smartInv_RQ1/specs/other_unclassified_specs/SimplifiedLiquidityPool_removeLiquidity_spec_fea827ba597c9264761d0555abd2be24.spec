pragma solidity 0.8.0;

contract SimplifiedLiquidityPool {mapping(address => mapping(address => uint256)) public liquidityBalance;

function removeLiquidity(address,address,uint256) public  {}

rule LiquidityBalanceConsistency() {
    address $token;
    address $to;
    uint256 $amount;
    require(liquidityBalance[$token][$to] >= $amount);

    uint256 balanceBefore = liquidityBalance[$token][$to];
    removeLiquidity($token, $to, $amount);

    assert(liquidityBalance[$token][$to] == balanceBefore - $amount);
}}