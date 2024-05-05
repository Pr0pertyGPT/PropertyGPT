pragma solidity 0.8.0;

contract SimplifiedLiquidityPool {mapping(address => mapping(address => uint256)) public liquidityBalance;

function removeLiquidity(address,address,uint256) public  {}

rule LiquidityDecreasesOnRemoval(){
    address $token;
    address $to;
    uint256 $amount;
    uint256 initialLiquidityBalance = liquidityBalance[$token][$to];
    removeLiquidity($token, $to, $amount);

    assert(liquidityBalance[$token][$to] == initialLiquidityBalance - $amount);
}}