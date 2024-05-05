pragma solidity 0.8.0;

contract SimplifiedLiquidityPool {mapping(address => mapping(address => uint256)) public liquidityBalance;

function addLiquidity(address,uint256) public  {}

rule ValidateNoChangeToOtherLiquidity() {
    address $token;
    uint256 $amount;
    address $liquidityProvider;
    address $otherLiquidityProvider;

    require($otherLiquidityProvider != $liquidityProvider);

    uint256 liquidityBalanceBefore = liquidityBalance[$token][$otherLiquidityProvider];
    addLiquidity($token, $amount);

    assert(liquidityBalanceBefore == liquidityBalance[$token][$otherLiquidityProvider]);
}}