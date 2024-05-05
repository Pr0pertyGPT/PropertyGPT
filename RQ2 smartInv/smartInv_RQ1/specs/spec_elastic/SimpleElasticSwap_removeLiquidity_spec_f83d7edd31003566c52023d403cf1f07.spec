pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function removeLiquidity(uint256) public  {}

rule ValidateLiquidityRemovalEffects() {
    uint256 $liquidity;
    address $sender;
    
    require($liquidity > 0 && $liquidity <= liquidityBalance[$sender]);
    require(totalLiquidity > 0);

    uint256 balanceBaseTokenBefore = baseTokenReserve;
    uint256 balanceQuoteTokenBefore = quoteTokenReserve;
    uint256 totalLiquidityBefore = totalLiquidity;
    uint256 senderLiquidityBalanceBefore = liquidityBalance[$sender];

    removeLiquidity($liquidity);

    uint256 baseAmount = ($liquidity * balanceBaseTokenBefore) / totalLiquidityBefore;
    uint256 quoteAmount = ($liquidity * balanceQuoteTokenBefore) / totalLiquidityBefore;

    assert(baseTokenReserve == balanceBaseTokenBefore - baseAmount);
    assert(quoteTokenReserve == balanceQuoteTokenBefore - quoteAmount);
    assert(totalLiquidity == totalLiquidityBefore - $liquidity);
    assert(liquidityBalance[$sender] == senderLiquidityBalanceBefore - $liquidity);
}}