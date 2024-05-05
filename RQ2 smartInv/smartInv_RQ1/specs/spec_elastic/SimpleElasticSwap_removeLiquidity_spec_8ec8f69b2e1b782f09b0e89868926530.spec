pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function removeLiquidity(uint256) public  {}

rule VerifyLiquidityRemovalBalances() {
    address $sender;
    uint256 $liquidity;
    uint256 liquidityBalanceBefore = liquidityBalance[$sender];
    uint256 totalLiquidityBefore = totalLiquidity;
    
    uint256 baseTokenReserveBefore = baseTokenReserve;
    uint256 quoteTokenReserveBefore = quoteTokenReserve;
    
    removeLiquidity($liquidity);

    uint256 baseAmount = ($liquidity * baseTokenReserveBefore) / totalLiquidityBefore;
    uint256 quoteAmount = ($liquidity * quoteTokenReserveBefore) / totalLiquidityBefore;

    assert(liquidityBalance[$sender] == liquidityBalanceBefore - $liquidity);
    assert(totalLiquidity == totalLiquidityBefore - $liquidity);
    assert(baseTokenReserve == baseTokenReserveBefore - baseAmount);
    assert(quoteTokenReserve == quoteTokenReserveBefore - quoteAmount);
}}