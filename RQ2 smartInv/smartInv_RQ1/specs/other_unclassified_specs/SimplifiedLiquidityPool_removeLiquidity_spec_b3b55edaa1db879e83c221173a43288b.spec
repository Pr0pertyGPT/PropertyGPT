pragma solidity 0.8.0;

contract SimplifiedLiquidityPool {mapping(address => mapping(address => uint256)) public liquidityBalance;

function removeLiquidity(address,address,uint256) public  {}

rule EnsureLiquidityReductionCorrectness() {
    address $token;
    address $to;
    uint256 $amount;
    uint256 liquidityBalanceBefore = liquidityBalance[$token][$to];
    require(liquidityBalance[$token][$to] >= $amount);

    removeLiquidity($token, $to, $amount);

    assert(liquidityBalanceBefore - $amount == liquidityBalance[$token][$to]);
}}