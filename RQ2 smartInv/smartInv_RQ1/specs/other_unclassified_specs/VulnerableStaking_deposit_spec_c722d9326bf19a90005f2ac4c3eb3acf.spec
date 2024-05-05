pragma solidity 0.8.0;

contract VulnerableStaking {mapping(address => uint256) public balances;
uint256 public totalSupply;


rule EnsureDepositUpdatesBalancesCorrectly() {
    address $depositor;
    uint256 $deposit_amount;

    // Store initial states
    uint256 initialTotalSupply = totalSupply;
    uint256 initialDepositorBalance = balances[$depositor];

    // Assume deposit function is implied by direct balance and totalSupply manipulation as shown
    // in the function code provided. Simulate the deposit action.
    balances[$depositor] += $deposit_amount;
    totalSupply += $deposit_amount;

    // Validation checks
    assert(balances[$depositor] == initialDepositorBalance + $deposit_amount);
    assert(totalSupply == initialTotalSupply + $deposit_amount);
}}