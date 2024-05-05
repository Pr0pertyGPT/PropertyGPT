pragma solidity 0.8.0;

contract SimplifiedLiquidityPool {mapping(address => mapping(address => uint256)) public liquidityBalance;

function addLiquidity(address,uint256) public  {}

rule AddLiquidityIncreasesBalanceProportionally() {
    address $token;
    address $liquidityProvider;
    uint256 $amount;

    uint256 initialBalance = liquidityBalance[$token][$liquidityProvider];
    addLiquidity($token, $amount);

    assert(liquidityBalance[$token][$liquidityProvider] == initialBalance + $amount);
}}