pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function deposit(uint256) public  {}

rule VerifyDepositFunctionality() {
    address $sender;
    uint256 $amount;
    uint256 balancesSenderBefore = balances[$sender];
    uint256 balancesContractBefore = balances[address(this)];
    uint256 totalLiquidityBefore = totalLiquidity;
    deposit($amount);

    assert(balances[$sender] == balancesSenderBefore + $amount);
    assert(balances[address(this)] == balancesContractBefore + $amount);
    assert(totalLiquidity == totalLiquidityBefore + $amount);
}}