pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function deposit(uint256) public  {}

rule TestDepositFunctionConsistency() {
    address $user;
    uint256 $depositAmount;
    uint256 userBalanceBefore = balances[$user];
    uint256 contractBalanceBefore = balances[address(this)];
    uint256 liquidityBefore = totalLiquidity;
    
    deposit($depositAmount);

    assert(balances[$user] == userBalanceBefore + $depositAmount);
    assert(balances[address(this)] == contractBalanceBefore + $depositAmount);
    assert(totalLiquidity == liquidityBefore + $depositAmount);
}}