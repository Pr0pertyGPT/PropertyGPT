pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function removeLiquidity(uint256) public  {}

rule RemoveLiquidityConservesTotalValue() {
    address $sender;
    uint256 $liquidity;
    require($liquidity > 0 && $liquidity <= liquidityBalance[$sender], "Invalid liquidity amount");
    require(totalLiquidity > 0, "No liquidity available");

    uint256 totalLiquidityBefore = totalLiquidity;
    uint256 senderLiquidityBalanceBefore = liquidityBalance[$sender];

    uint256 baseTokenReserveBefore = baseTokenReserve;
    uint256 quoteTokenReserveBefore = quoteTokenReserve;

    removeLiquidity($liquidity);

    uint256 baseTokenReserveAfter = baseTokenReserve;
    uint256 quoteTokenReserveAfter = quoteTokenReserve;
    uint256 totalLiquidityAfter = totalLiquidity;
    uint256 senderLiquidityBalanceAfter = liquidityBalance[$sender];

    assert(senderLiquidityBalanceBefore - $liquidity == senderLiquidityBalanceAfter);
    assert(totalLiquidityBefore - $liquidity == totalLiquidityAfter);
    assert(baseTokenReserveBefore - (baseTokenReserveBefore * $liquidity / totalLiquidityBefore) == baseTokenReserveAfter);
    assert(quoteTokenReserveBefore - (quoteTokenReserveBefore * $liquidity / totalLiquidityBefore) == quoteTokenReserveAfter);
}}