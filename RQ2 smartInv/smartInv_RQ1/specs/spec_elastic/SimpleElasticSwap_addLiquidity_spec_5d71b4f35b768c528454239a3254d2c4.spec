pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function addLiquidity(uint256,uint256) public  {}

rule CheckLiquidityAfterAddition() {
    uint256 baseAmount;
    uint256 quoteAmount;
    address sender;

    uint256 baseTokenReserveBefore = baseTokenReserve;
    uint256 quoteTokenReserveBefore = quoteTokenReserve;
    uint256 totalLiquidityBefore = totalLiquidity;
    uint256 liquidityBalanceBefore = liquidityBalance[sender];
    
    addLiquidity(baseAmount, quoteAmount);
    
    uint256 expectedLiquidityIssued;
    if (totalLiquidityBefore == 0) {
        expectedLiquidityIssued = baseAmount + quoteAmount;
    } else {
        expectedLiquidityIssued = ((baseAmount + quoteAmount) * totalLiquidityBefore) / (baseTokenReserveBefore + quoteTokenReserveBefore);
    }
    
    assert(baseTokenReserve == baseTokenReserveBefore + baseAmount);
    assert(quoteTokenReserve == quoteTokenReserveBefore + quoteAmount);
    assert(totalLiquidity == totalLiquidityBefore + expectedLiquidityIssued);
    assert(liquidityBalance[sender] == liquidityBalanceBefore + expectedLiquidityIssued);
}}