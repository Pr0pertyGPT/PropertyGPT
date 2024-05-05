pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function addLiquidity(uint256,uint256) public  {}

rule EnsureAddLiquidityIncreasesReservesProportionally() {
    uint256 $baseAmount;
    uint256 $quoteAmount;
    address $sender;

    require($baseAmount > 0 && $quoteAmount > 0);

    uint256 totalLiquidityBefore = totalLiquidity;
    uint256 baseTokenReserveBefore = baseTokenReserve;
    uint256 quoteTokenReserveBefore = quoteTokenReserve;
    uint256 liquidityBalanceBefore = liquidityBalance[$sender];

    addLiquidity($baseAmount, $quoteAmount);

    uint256 liquidityIssued = totalLiquidity - totalLiquidityBefore;
    uint256 newBaseTokenReserve = baseTokenReserve;
    uint256 newQuoteTokenReserve = quoteTokenReserve;
    uint256 newLiquidityBalance = liquidityBalance[$sender];

    assert(newBaseTokenReserve == baseTokenReserveBefore + $baseAmount);
    assert(newQuoteTokenReserve == quoteTokenReserveBefore + $quoteAmount);
    if(totalLiquidityBefore == 0) {
        assert(liquidityIssued == $baseAmount + $quoteAmount);
    } else {
        assert(liquidityIssued * (baseTokenReserveBefore + quoteTokenReserveBefore) == ($baseAmount + $quoteAmount) * totalLiquidityBefore);
    }
    assert(newLiquidityBalance == liquidityBalanceBefore + liquidityIssued);
}}