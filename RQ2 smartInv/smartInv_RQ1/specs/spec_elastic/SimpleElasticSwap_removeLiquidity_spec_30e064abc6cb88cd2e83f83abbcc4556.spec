pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function removeLiquidity(uint256) public  {}

rule EnsureValidLiquidityRemoval() {
    uint256 $liquidity;
    uint256 $initial_liquidityBalance;
    uint256 $initial_totalLiquidity;
    uint256 $initial_baseTokenReserve;
    uint256 $initial_quoteTokenReserve;

    liquidityBalance[msg.sender] = $initial_liquidityBalance;
    totalLiquidity = $initial_totalLiquidity;
    baseTokenReserve = $initial_baseTokenReserve;
    quoteTokenReserve = $initial_quoteTokenReserve;

    require($liquidity > 0 && $liquidity <= liquidityBalance[msg.sender]);
    require(totalLiquidity > 0);

    uint256 $baseAmount = ($liquidity * baseTokenReserve) / totalLiquidity;
    uint256 $quoteAmount = ($liquidity * quoteTokenReserve) / totalLiquidity;

    removeLiquidity($liquidity);

    assert(liquidityBalance[msg.sender] == $initial_liquidityBalance - $liquidity);
    assert(totalLiquidity == $initial_totalLiquidity - $liquidity);
    assert(baseTokenReserve == $initial_baseTokenReserve - $baseAmount);
    assert(quoteTokenReserve == $initial_quoteTokenReserve - $quoteAmount);
}}