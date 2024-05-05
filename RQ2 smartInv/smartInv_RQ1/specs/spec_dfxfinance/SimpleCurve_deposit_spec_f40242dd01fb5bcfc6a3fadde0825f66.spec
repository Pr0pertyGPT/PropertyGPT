pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function deposit(uint256) public  {}

rule DepositLiquidityInvariant() {
    address $depositor;
    uint256 $amount;

    uint256 balanceOfDepositorBefore = balances[$depositor];
    uint256 balanceOfContractBefore = balances[address(this)];
    uint256 totalLiquidityBefore = totalLiquidity;

    deposit($amount);

    assert(balances[$depositor] == balanceOfDepositorBefore + $amount);
    assert(balances[address(this)] == balanceOfContractBefore + $amount);
    assert(totalLiquidity == totalLiquidityBefore + $amount);
}}