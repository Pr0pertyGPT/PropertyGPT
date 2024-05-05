pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function flashLoan(uint256) public  {}

rule RestoreContractBalanceAfterLoan() {
    uint256 $loan_amount;
    uint256 initContractBalance = balances[address(this)];

    __assume__(balances[address(this)] >= $loan_amount);
    flashLoan($loan_amount);
    assert(balances[address(this)] == initContractBalance);
}}