pragma solidity 0.5.17;

contract VulnerableBatchTransfer {mapping(address => uint256) public balances;

function batchTransfer(address[],uint256) public returns(bool) {}

rule checkBatchTransferSafety() {
    // Example setup for symbolic execution
    address[] memory symbolicReceivers = new address[](3); // Simulated list of three receivers
    uint256 symbolicValue = 5; // Simulated transfer value to each receiver

    // Simulate initial balances
    uint256 senderInitialBalance = balances[msg.sender];
    uint256[] memory receiversInitialBalances = new uint256[](symbolicReceivers.length);
    for (uint i = 0; i < symbolicReceivers.length; i++) {
        receiversInitialBalances[i] = balances[symbolicReceivers[i]];
    }

    // Calculate expected total transfer amount
    uint256 expectedTotalAmount = symbolicValue * symbolicReceivers.length;
    require(senderInitialBalance >= expectedTotalAmount, "Sender has insufficient balance");

    // Execute the batch transfer
    batchTransfer(symbolicReceivers, symbolicValue);

    // Verify sender's balance after transfer
    assert(balances[msg.sender] == senderInitialBalance - expectedTotalAmount);

    // Verify each receiver's balance increment
    for (uint j = 0; j < symbolicReceivers.length; j++) {
        assert(balances[symbolicReceivers[j]] == receiversInitialBalances[j] + symbolicValue);
    }

    // Check against overflow in total transfer calculation
    assert(expectedTotalAmount / symbolicValue == symbolicReceivers.length);
}}