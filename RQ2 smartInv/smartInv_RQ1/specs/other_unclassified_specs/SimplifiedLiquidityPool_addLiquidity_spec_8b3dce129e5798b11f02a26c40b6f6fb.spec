pragma solidity 0.8.0;

contract SimplifiedLiquidityPool {mapping(address => mapping(address => uint256)) public liquidityBalance;

function addLiquidity(address,uint256) public  {}

rule VerifyAddLiquidityInvariant() {
    address $token;
    address $user;
    uint256 $amount;

    uint256 liquidityBefore = liquidityBalance[$token][$user];
    addLiquidity($token, $amount);
    uint256 liquidityAfter = liquidityBalance[$token][$user];

    assert(liquidityBefore + $amount == liquidityAfter);
}}