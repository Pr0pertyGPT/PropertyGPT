pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function flashLoan(uint256) public  {}

rule FlashLoanRepaymentIntegrity() {
    uint256 $loanAmount;
    __assume__(balances[address(this)] >= $loanAmount);

    uint256 balanceThisBefore = balances[address(this)];
    uint256 balanceSenderBefore = balances[msg.sender];
    bool isBorrowedSenderBefore = isBorrowed[msg.sender];

    flashLoan($loanAmount);

    uint256 balanceThisAfter = balances[address(this)];
    uint256 balanceSenderAfter = balances[msg.sender];
    bool isBorrowedSenderAfter = isBorrowed[msg.sender];

    // Checking if balances are correctly updated after flash loan
    assert(balanceThisBefore == balanceThisAfter);
    assert(balanceSenderBefore + $loanAmount == balanceSenderAfter);
    // Ensuring flashLoan status is reverted back to false after operation
    assert(isBorrowedSenderBefore == false && isBorrowedSenderAfter == false);
}}