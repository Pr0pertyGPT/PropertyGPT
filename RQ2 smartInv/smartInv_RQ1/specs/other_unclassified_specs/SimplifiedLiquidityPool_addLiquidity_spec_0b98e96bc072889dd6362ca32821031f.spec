pragma solidity 0.8.0;

contract SimplifiedLiquidityPool {mapping(address => mapping(address => uint256)) public liquidityBalance;

function addLiquidity(address,uint256) public  {}

rule AddLiquidityDoesNotImpactUnrelatedTokenBalances() {
    address $token;
    address $otherToken;
    address $user;
    uint256 $amount;

    require($otherToken != $token);

    uint256 otherTokenBalanceBefore = liquidityBalance[$otherToken][$user];
    addLiquidity($token, $amount);
    uint256 otherTokenBalanceAfter = liquidityBalance[$otherToken][$user];

    assert(otherTokenBalanceBefore == otherTokenBalanceAfter);
}}