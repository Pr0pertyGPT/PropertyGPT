pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function removeLiquidity(uint256) public  {}

rule PreserveTotalLiquidityInvariant() {
    uint256 $initialLiquidity;
    uint256 $liquidityToRemove;
    totalLiquidity = $initialLiquidity;
    uint256 totalLiquidityBefore = totalLiquidity;
    
    removeLiquidity($liquidityToRemove);

    assert(totalLiquidity + $liquidityToRemove == totalLiquidityBefore);
}}