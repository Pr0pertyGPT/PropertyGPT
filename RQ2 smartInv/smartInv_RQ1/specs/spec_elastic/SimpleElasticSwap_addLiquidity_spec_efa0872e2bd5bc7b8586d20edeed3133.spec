pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function addLiquidity(uint256,uint256) public  {}

rule ValidateLiquidityAddition() {
    uint256 $baseAmount;
    uint256 $quoteAmount;
    address $sender;

    uint256 liquidityBefore = totalLiquidity;
    uint256 baseReserveBefore = baseTokenReserve;
    uint256 quoteReserveBefore = quoteTokenReserve;
    uint256 senderLiquidityBalanceBefore = liquidityBalance[$sender];
    
    addLiquidity($baseAmount, $quoteAmount);

    uint256 baseReserveAfter = baseTokenReserve;
    uint256 quoteReserveAfter = quoteTokenReserve;
    uint256 liquidityAfter = totalLiquidity;
    uint256 senderLiquidityBalanceAfter = liquidityBalance[$sender];

    if (liquidityBefore == 0) {
        assert(liquidityAfter == $baseAmount + $quoteAmount);
    } else {
        assert(liquidityAfter == liquidityBefore + (($baseAmount + $quoteAmount) * liquidityBefore) / (baseReserveBefore + quoteReserveBefore));
    }

    assert(baseReserveAfter == baseReserveBefore + $baseAmount);
    assert(quoteReserveAfter == quoteReserveBefore + $quoteAmount);
    assert(senderLiquidityBalanceAfter == senderLiquidityBalanceBefore + liquidityAfter - liquidityBefore);
}}