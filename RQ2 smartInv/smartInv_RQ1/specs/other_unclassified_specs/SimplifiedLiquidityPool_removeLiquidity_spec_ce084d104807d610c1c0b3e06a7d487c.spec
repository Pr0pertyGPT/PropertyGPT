pragma solidity 0.8.0;

contract SimplifiedLiquidityPool {mapping(address => mapping(address => uint256)) public liquidityBalance;

function removeLiquidity(address,address,uint256) public  {}

rule LiquidityBalanceDecreasesCorrectly() {
    address $token;
    address $to;
    uint256 $init_liquidity;
    liquidityBalance[$token][$to] = $init_liquidity;
    uint256 $amount;

    require($amount <= $init_liquidity);

    uint256 balanceBefore = liquidityBalance[$token][$to];
    removeLiquidity($token, $to, $amount);

    assert(liquidityBalance[$token][$to] == balanceBefore - $amount);
}}