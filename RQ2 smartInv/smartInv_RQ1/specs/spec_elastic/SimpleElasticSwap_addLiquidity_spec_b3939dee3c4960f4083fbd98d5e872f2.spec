pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;


rule ValidateLiquidityAmountsNotZero() {
    uint256 $baseAmount;
    uint256 $quoteAmount;
    require($baseAmount > 0 && $quoteAmount > 0);
}}