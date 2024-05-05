pragma solidity 0.8.0;

contract SimplifiedLiquidityPool {mapping(address => mapping(address => uint256)) public liquidityBalance;

function addLiquidity(address,uint256) public  {}

rule ValidateLiquidityIncrease() {
    address $token;
    address $sender;
    uint256 $amount;

    uint256 balanceBefore = liquidityBalance[$token][$sender];
    addLiquidity($token, $amount);
    assert(liquidityBalance[$token][$sender] == balanceBefore + $amount);
}}