pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function deposit(uint256) public  {}

rule DepositIncreasesBalancesCorrectly() {
    uint256 $amount;
    address $depositor = msg.sender;
    uint256 balanceBefore = balances[$depositor];
    uint256 contractBalanceBefore = balances[address(this)];
    uint256 totalLiquidityBefore = totalLiquidity;
    
    deposit($amount);

    assert(balances[$depositor] == balanceBefore + $amount);
    assert(balances[address(this)] == contractBalanceBefore + $amount);
    assert(totalLiquidity == totalLiquidityBefore + $amount);
}}