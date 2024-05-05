pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function removeLiquidity(uint256) public  {}

rule LiquidityRemovalConservesTotalSupply() {
    uint256 $liquidityToRemove;
    uint256 totalLiquidityBefore = totalLiquidity;
    uint256 baseTokenReserveBefore = baseTokenReserve;
    uint256 quoteTokenReserveBefore = quoteTokenReserve;
    uint256 totalSupplyBefore = baseTokenReserve + quoteTokenReserve;
    address $account;

    liquidityBalance[$account] = $liquidityToRemove;
    require($liquidityToRemove > 0 && $liquidityToRemove <= liquidityBalance[$account]);
    require(totalLiquidity > 0);

    removeLiquidity($liquidityToRemove);

    uint256 totalSupplyAfter = baseTokenReserve + quoteTokenReserve;
    uint256 totalLiquidityAfter = totalLiquidity;
    uint256 baseTokenReserveAfter = baseTokenReserve;
    uint256 quoteTokenReserveAfter = quoteTokenReserve;

    assert(totalSupplyBefore == totalSupplyAfter);
    assert(totalLiquidityBefore == (totalLiquidityAfter + $liquidityToRemove));
    assert(baseTokenReserveBefore >= baseTokenReserveAfter);
    assert(quoteTokenReserveBefore >= quoteTokenReserveAfter);
}}