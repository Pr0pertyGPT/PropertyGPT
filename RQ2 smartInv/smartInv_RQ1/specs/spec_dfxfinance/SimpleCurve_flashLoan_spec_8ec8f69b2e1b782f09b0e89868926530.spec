pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function flashLoan(uint256) public  {}

rule FlashLoanRepaymentVerification() {
    uint256 $amount;
    address $borrower = msg.sender;
    uint256 balanceBorrowerBefore = balances[$borrower];
    uint256 balanceContractBefore = balances[address(this)];
    bool isBorrowedBefore = isBorrowed[$borrower];

    __assume__(isBorrowedBefore == false);
    flashLoan($amount);

    assert(balances[$borrower] == balanceBorrowerBefore + $amount);
    assert(balances[address(this)] == balanceContractBefore - $amount);
    assert(isBorrowed[$borrower] == true);

    // Emulate user action that would change the balances to repay the loan.
    balances[$borrower] -= $amount;
    balances[address(this)] += $amount;
    flashLoan($amount);

    assert(balances[$borrower] == balanceBorrowerBefore);
    assert(balances[address(this)] == balanceContractBefore);
    assert(isBorrowed[$borrower] == false);
}}