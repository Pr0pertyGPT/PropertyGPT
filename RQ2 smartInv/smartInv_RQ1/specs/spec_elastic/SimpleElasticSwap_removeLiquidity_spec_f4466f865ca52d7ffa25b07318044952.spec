pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function removeLiquidity(uint256) public  {}

rule InvalidLiquidityDoesNotAlterState() {
    uint256 $liquidity;
    address $sender;
    uint256 liquidityBefore = liquidityBalance[$sender];
    uint256 baseTokenReserveBefore = baseTokenReserve;
    uint256 quoteTokenReserveBefore = quoteTokenReserve;
    uint256 totalLiquidityBefore = totalLiquidity;

    require($liquidity <= 0 || $liquidity > liquidityBalance[$sender]);
    // attempting to remove invalid liquidity amount
    removeLiquidity($liquidity);
  
    assert(liquidityBalance[$sender] == liquidityBefore);
    assert(baseTokenReserve == baseTokenReserveBefore);
    assert(quoteTokenReserve == quoteTokenReserveBefore);
    assert(totalLiquidity == totalLiquidityBefore);
}}