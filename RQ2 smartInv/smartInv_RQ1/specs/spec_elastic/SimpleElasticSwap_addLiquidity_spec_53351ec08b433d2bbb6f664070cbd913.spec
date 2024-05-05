pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function addLiquidity(uint256,uint256) public  {}

rule VerifyBaseAndQuoteAmountsPositive() {
    uint256 $baseAmount;
    uint256 $quoteAmount;
    require($baseAmount > 0 && $quoteAmount > 0);
    addLiquidity($baseAmount, $quoteAmount);
    assert($baseAmount > 0 && $quoteAmount > 0);
}}