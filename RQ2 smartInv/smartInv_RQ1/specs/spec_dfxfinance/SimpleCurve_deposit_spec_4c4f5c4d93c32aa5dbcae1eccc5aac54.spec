pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function deposit(uint256) public  {}

rule DepositBalanceUpdateCorrectly() {
    uint256 $amount;
    address $sender = msg.sender;
    uint256 balanceBeforeSender = balances[$sender];
    uint256 balanceBeforeContract = balances[address(this)];
    uint256 totalLiquidityBefore = totalLiquidity;

    deposit($amount);

    assert(balances[$sender] == balanceBeforeSender + $amount);
    assert(balances[address(this)] == balanceBeforeContract + $amount);
    assert(totalLiquidity == totalLiquidityBefore + $amount);
}}