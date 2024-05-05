pragma solidity 0.8.0;

contract SimpleCurve {mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;

function deposit(uint256) public  {}

rule DepositAmountReflectedInBalancesAndTotalLiquidity() {
    address $depositor;
    uint256 $depositAmount;
    uint256 balanceOfDepositorBefore = balances[$depositor];
    uint256 balanceOfContractBefore = balances[address(this)];
    uint256 totalLiquidityBefore = totalLiquidity;

    deposit($depositAmount);

    uint256 balanceOfDepositorAfter = balances[$depositor];
    uint256 balanceOfContractAfter = balances[address(this)];
    uint256 totalLiquidityAfter = totalLiquidity;

    // Checking depositor's balance is correctly updated
    assert(balanceOfDepositorBefore + $depositAmount == balanceOfDepositorAfter);
    // Checking contract's balance is correctly updated
    assert(balanceOfContractBefore + $depositAmount == balanceOfContractAfter);
    // Checking total liquidity is correctly updated
    assert(totalLiquidityBefore + $depositAmount == totalLiquidityAfter);
}}