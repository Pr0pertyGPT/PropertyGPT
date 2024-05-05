pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function addLiquidity(uint256,uint256) public  {}

rule EnsureLiquidityAdditionIsCorrect() {
    uint256 $baseAmount;
    uint256 $quoteAmount;
    address $sender;

    require($baseAmount > 0 && $quoteAmount > 0);

    uint256 liquidityBefore = totalLiquidity;
    uint256 baseTokenReserveBefore = baseTokenReserve;
    uint256 quoteTokenReserveBefore = quoteTokenReserve;
    uint256 liquidityBalanceBefore = liquidityBalance[$sender];

    addLiquidity($baseAmount, $quoteAmount);

    uint256 liquidityIssued;
    if (totalLiquidity == 0) {
        liquidityIssued = $baseAmount + $quoteAmount;
    } else {
        liquidityIssued = (($baseAmount + $quoteAmount) * totalLiquidity) / (baseTokenReserveBefore + quoteTokenReserveBefore);
    }

    assert(baseTokenReserve == baseTokenReserveBefore + $baseAmount);
    assert(quoteTokenReserve == quoteTokenReserveBefore + $quoteAmount);
    assert(totalLiquidity == liquidityBefore + liquidityIssued);
    assert(liquidityBalance[$sender] == liquidityBalanceBefore + liquidityIssued);
}}