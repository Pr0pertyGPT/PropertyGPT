pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function addLiquidity(uint256,uint256) public  {}

rule VerifyLiquidityIncreaseProportionally() {
    uint256 $baseAmount;
    uint256 $quoteAmount;
    uint256 baseTokenReserveBefore = baseTokenReserve;
    uint256 quoteTokenReserveBefore = quoteTokenReserve;
    uint256 totalLiquidityBefore = totalLiquidity;

    addLiquidity($baseAmount, $quoteAmount);

    uint256 baseTokenReserveAfter = baseTokenReserve;
    uint256 quoteTokenReserveAfter = quoteTokenReserve;
    uint256 totalLiquidityAfter = totalLiquidity;
    
    if(totalLiquidityBefore == 0) {
        assert(totalLiquidityAfter == $baseAmount + $quoteAmount);
    } else {
        assert(((baseTokenReserveAfter - baseTokenReserveBefore) + (quoteTokenReserveAfter - quoteTokenReserveBefore)) * totalLiquidityBefore == (totalLiquidityAfter - totalLiquidityBefore) * (baseTokenReserveBefore + quoteTokenReserveBefore));
    }

    uint256 liquidityBalanceAfter = liquidityBalance[msg.sender];
    assert(liquidityBalanceAfter - (totalLiquidityBefore == 0 ? 0 : totalLiquidityBefore) == totalLiquidityAfter - totalLiquidityBefore);
}}