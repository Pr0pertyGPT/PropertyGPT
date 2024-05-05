pragma solidity 0.8.0;

contract SimplifiedLiquidityPool {mapping(address => mapping(address => uint256)) public liquidityBalance;

function removeLiquidity(address,address,uint256) public  {}

rule CheckLiquidityReductionConsistency() {
    address $token;
    address $to;
    uint256 $amount;

    uint256 liquidityBalanceBefore = liquidityBalance[$token][$to];
    removeLiquidity($token, $to, $amount);
    uint256 liquidityBalanceAfter = liquidityBalance[$token][$to];

    assert(liquidityBalanceBefore == liquidityBalanceAfter + $amount);
}}