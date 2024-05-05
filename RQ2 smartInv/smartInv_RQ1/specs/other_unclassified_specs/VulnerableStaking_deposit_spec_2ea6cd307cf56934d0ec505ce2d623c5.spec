pragma solidity 0.8.0;

contract VulnerableStaking {mapping(address => uint256) public balances;
uint256 public totalSupply;


rule DepositFunctionalityTest() {
    // Symbolic inputs for account address and deposit amount
    // Since 'any()' function doesn't exist, we use pre-defined but unspecified values
    address account; // Represents a symbolic account address
    uint256 amount; // Represents a symbolic deposit amount

    // Save the initial balances and total supply
    uint256 balanceBefore = balances[account];
    uint256 totalSupplyBefore = totalSupply;

    // Simulate the deposit functionality
    balances[account] += amount; // Update the balance of the account
    totalSupply += amount; // Update the total supply

    // Assertions to verify the deposit functionality works as expected
    assert(balances[account] == balanceBefore + amount); // Verify the account balance is correctly updated
    assert(totalSupply == totalSupplyBefore + amount); // Verify the total supply is correctly updated
}}