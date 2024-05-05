pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function addLiquidity(uint256,uint256) public  {}

rule LiquidityAmountsMustIncrease() {
    uint256 $baseAmount;
    uint256 $quoteAmount;
    address $user;

    require($baseAmount > 0 && $quoteAmount > 0);

    uint256 baseTokenReserveBefore = baseTokenReserve;
    uint256 quoteTokenReserveBefore = quoteTokenReserve;
    uint256 totalLiquidityBefore = totalLiquidity;
    uint256 userLiquidityBalanceBefore = liquidityBalance[$user];

    addLiquidity($baseAmount, $quoteAmount);

    assert(baseTokenReserve > baseTokenReserveBefore);
    assert(quoteTokenReserve > quoteTokenReserveBefore);
    assert(totalLiquidity > totalLiquidityBefore);
    assert(liquidityBalance[$user] > userLiquidityBalanceBefore);
}}