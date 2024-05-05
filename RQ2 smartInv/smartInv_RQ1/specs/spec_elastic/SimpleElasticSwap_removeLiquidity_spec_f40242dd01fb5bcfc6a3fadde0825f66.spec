pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function removeLiquidity(uint256) public  {}

rule VerifyLiquidityRemovalEffects() {
    address $user;
    uint256 $liquidityRemoved;
    require($liquidityRemoved > 0 && $liquidityRemoved <= liquidityBalance[$user], "Invalid liquidity amount");
    require(totalLiquidity > 0, "No liquidity available");

    uint256 liquidityBalanceOfUserBefore = liquidityBalance[$user];
    uint256 totalLiquidityBefore = totalLiquidity;
    uint256 baseTokenReserveBefore = baseTokenReserve;
    uint256 quoteTokenReserveBefore = quoteTokenReserve;

    removeLiquidity($liquidityRemoved);

    uint256 baseAmount = ($liquidityRemoved * baseTokenReserveBefore) / totalLiquidityBefore;
    uint256 quoteAmount = ($liquidityRemoved * quoteTokenReserveBefore) / totalLiquidityBefore;

    assert(liquidityBalance[$user] == liquidityBalanceOfUserBefore - $liquidityRemoved);
    assert(totalLiquidity == totalLiquidityBefore - $liquidityRemoved);
    assert(baseTokenReserve == baseTokenReserveBefore - baseAmount);
    assert(quoteTokenReserve == quoteTokenReserveBefore - quoteAmount);
}}