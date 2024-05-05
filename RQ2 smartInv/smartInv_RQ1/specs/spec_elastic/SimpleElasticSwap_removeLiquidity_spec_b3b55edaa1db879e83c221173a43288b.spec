pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function removeLiquidity(uint256) public  {}

rule ValidateLiquidityReductionIntegrity() {
    uint256 $liquidity;
    address $sender;
    uint256 balanceBefore = liquidityBalance[$sender];
    uint256 baseTokenReserveBefore = baseTokenReserve;
    uint256 quoteTokenReserveBefore = quoteTokenReserve;
    uint256 totalLiquidityBefore = totalLiquidity;
    uint256 baseAmountCalculated = ($liquidity * baseTokenReserve) / totalLiquidity;
    uint256 quoteAmountCalculated = ($liquidity * quoteTokenReserve) / totalLiquidity;

    removeLiquidity($liquidity);

    assert(liquidityBalance[$sender] == balanceBefore - $liquidity);
    assert(baseTokenReserve == baseTokenReserveBefore - baseAmountCalculated);
    assert(quoteTokenReserve == quoteTokenReserveBefore - quoteAmountCalculated);
    assert(totalLiquidity == totalLiquidityBefore - $liquidity);
}}