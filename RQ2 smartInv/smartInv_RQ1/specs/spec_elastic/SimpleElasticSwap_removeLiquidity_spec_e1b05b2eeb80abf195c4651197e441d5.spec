pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function removeLiquidity(uint256) public  {}

rule ValidateLiquidityRemoval() {
    uint256 $liquidity;
    require($liquidity > 0 && $liquidity <= liquidityBalance[msg.sender], "");
    require(totalLiquidity > 0, "");

    uint256 balanceBeforeBase = baseTokenReserve;
    uint256 balanceBeforeQuote = quoteTokenReserve;
    uint256 totalLiquidityBefore = totalLiquidity;
    uint256 senderLiquidityBalanceBefore = liquidityBalance[msg.sender];

    removeLiquidity($liquidity);

    uint256 baseAmountCalculated = ($liquidity * balanceBeforeBase) / totalLiquidityBefore;
    uint256 quoteAmountCalculated = ($liquidity * balanceBeforeQuote) / totalLiquidityBefore;

    assert(baseTokenReserve == balanceBeforeBase - baseAmountCalculated);
    assert(quoteTokenReserve == balanceBeforeQuote - quoteAmountCalculated);
    assert(totalLiquidity == totalLiquidityBefore - $liquidity);
    assert(liquidityBalance[msg.sender] == senderLiquidityBalanceBefore - $liquidity);
}}