pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function deposit(uint256) public  {}

rule DepositDoesNotDuplicateBalances() {
    uint256 $amount;
    uint256 balanceSenderBefore = balances[msg.sender];
    uint256 balanceContractBefore = balances[address(this)];
    uint256 totalLiquidityBefore = totalLiquidity;

    deposit($amount);

    assert(balances[msg.sender] == balanceSenderBefore + $amount);
    assert(balances[address(this)] == balanceContractBefore + $amount);
    assert(totalLiquidity == totalLiquidityBefore + $amount);
}}