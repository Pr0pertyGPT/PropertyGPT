pragma solidity 0.8.0;

contract SimplifiedLiquidityPool {mapping(address => mapping(address => uint256)) public liquidityBalance;

function addLiquidity(address,uint256) public  {}

rule VerifyAddLiquidityEffect() {
    address $token;
    address $contributor;
    uint256 $amountToAdd;
    
    uint256 liquidityBefore = liquidityBalance[$token][$contributor];
    
    addLiquidity($token, $amountToAdd);
    
    assert(liquidityBalance[$token][$contributor] == liquidityBefore + $amountToAdd);
}}