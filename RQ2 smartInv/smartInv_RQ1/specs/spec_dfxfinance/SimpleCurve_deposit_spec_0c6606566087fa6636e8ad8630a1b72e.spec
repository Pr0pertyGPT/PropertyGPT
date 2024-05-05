pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function deposit(uint256) public  {}

rule DepositIncreasesBalancesCorrectly() {
    address $depositor;
    uint256 $depositAmount;
    uint256 balanceBeforeDepositor = balances[$depositor];
    uint256 balanceBeforeContract = balances[address(this)];
    uint256 totalLiquidityBefore = totalLiquidity;
    
    deposit($depositAmount);

    assert(balances[$depositor] == balanceBeforeDepositor + $depositAmount);
    assert(balances[address(this)] == balanceBeforeContract + $depositAmount);
    assert(totalLiquidity == totalLiquidityBefore + $depositAmount);
}}