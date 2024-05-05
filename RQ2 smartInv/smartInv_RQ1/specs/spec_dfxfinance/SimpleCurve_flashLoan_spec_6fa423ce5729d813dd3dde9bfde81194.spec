pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function flashLoan(uint256) public  {}

rule VerifyFlashLoanEffectOnBalances() {
    uint256 $amount;
    address $holder;
    uint256 initBalanceHolder = balances[$holder];
    uint256 initBalanceContract = balances[address(this)];
    bool initIsBorrowedHolder = isBorrowed[$holder];

    __assume__(msg.sender == $holder);
    flashLoan($amount);

    assert(balances[$holder] == initBalanceHolder + $amount);
    assert(balances[address(this)] == initBalanceContract - $amount);
    assert(isBorrowed[$holder] == true);
    assert(isBorrowed[$holder] == !initIsBorrowedHolder);
}}