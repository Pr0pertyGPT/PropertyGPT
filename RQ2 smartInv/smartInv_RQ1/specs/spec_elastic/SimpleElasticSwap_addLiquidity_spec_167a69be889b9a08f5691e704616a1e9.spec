pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function addLiquidity(uint256,uint256) public  {}

rule ValidateLiquidityIncrease() {
    address $sender;
    uint256 $baseAmount;
    uint256 $quoteAmount;
    uint256 totalLiquidityBefore = totalLiquidity;
    uint256 baseTokenReserveBefore = baseTokenReserve;
    uint256 quoteTokenReserveBefore = quoteTokenReserve;
    uint256 liquidityBalanceBefore = liquidityBalance[$sender];
    
    require($baseAmount > 0 && $quoteAmount > 0);

    addLiquidity($baseAmount, $quoteAmount);

    if (totalLiquidityBefore == 0) {
        assert(totalLiquidity - totalLiquidityBefore == $baseAmount + $quoteAmount);
    } else {
        uint256 liquidityIssued = (($baseAmount + $quoteAmount) * totalLiquidityBefore) / (baseTokenReserveBefore + quoteTokenReserveBefore);
        assert(totalLiquidity - totalLiquidityBefore == liquidityIssued);
    }

    assert(baseTokenReserve - baseTokenReserveBefore == $baseAmount);
    assert(quoteTokenReserve - quoteTokenReserveBefore == $quoteAmount);
    assert(liquidityBalance[$sender] - liquidityBalanceBefore > 0);
}}