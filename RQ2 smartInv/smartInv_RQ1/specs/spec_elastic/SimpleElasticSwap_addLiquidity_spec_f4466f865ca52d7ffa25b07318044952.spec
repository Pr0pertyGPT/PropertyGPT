pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function addLiquidity(uint256,uint256) public  {}

rule LiquidityAmountsMustBePositive(){
    address $sender;
    uint256 $baseAmount;
    uint256 $quoteAmount;
    
    require($baseAmount > 0 && $quoteAmount > 0);

    uint256 liquidityBefore = totalLiquidity;
    uint256 baseReserveBefore = baseTokenReserve;
    uint256 quoteReserveBefore = quoteTokenReserve;
    uint256 senderLiquidityBefore = liquidityBalance[$sender];

    addLiquidity($baseAmount, $quoteAmount);

    uint256 liquidityAfter = totalLiquidity;
    uint256 baseReserveAfter = baseTokenReserve;
    uint256 quoteReserveAfter = quoteTokenReserve;
    uint256 senderLiquidityAfter = liquidityBalance[$sender];

    assert(liquidityAfter > liquidityBefore);
    assert(baseReserveAfter == baseReserveBefore + $baseAmount);
    assert(quoteReserveAfter == quoteReserveBefore + $quoteAmount);
    assert(senderLiquidityAfter > senderLiquidityBefore);
}}