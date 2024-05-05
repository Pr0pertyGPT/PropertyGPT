pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function addLiquidity(uint256,uint256) public  {}

rule AddLiquidityEnsuresPositiveInput() {
    uint256 $baseAmount;
    uint256 $quoteAmount;

    require($baseAmount > 0 && $quoteAmount > 0);

    uint256 totalLiquidityBefore = totalLiquidity;
    uint256 liquidityIssued;
    if (totalLiquidity == 0) {
        liquidityIssued = $baseAmount + $quoteAmount;
    } else {
        liquidityIssued = (($baseAmount + $quoteAmount) * totalLiquidity) / (baseTokenReserve + quoteTokenReserve);
    }

    addLiquidity($baseAmount, $quoteAmount);

    assert(totalLiquidity == totalLiquidityBefore + liquidityIssued);
}}