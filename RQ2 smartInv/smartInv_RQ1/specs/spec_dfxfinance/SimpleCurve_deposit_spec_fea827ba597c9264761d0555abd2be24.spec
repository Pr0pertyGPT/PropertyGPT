pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function deposit(uint256) public  {}

rule BalanceIncreasesOnDeposit() {
    address $depositor;
    uint256 $depositAmount;
    uint256 initBalanceDepositor = balances[$depositor];
    uint256 initBalanceContract = balances[address(this)];
    uint256 initTotalLiquidity = totalLiquidity;

    deposit($depositAmount);

    assert(balances[$depositor] == initBalanceDepositor + $depositAmount);
    assert(balances[address(this)] == initBalanceContract + $depositAmount);
    assert(totalLiquidity == initTotalLiquidity + $depositAmount);
}}