pragma solidity 0.5.17;

contract VulnerableBatchTransfer {mapping(address => uint256) public balances;

function batchTransfer(address[],uint256) public returns(bool) {}

rule VerifyBatchTransferIntegrity() {
    // Define symbolic variables for the number of receivers and amount per receiver
    uint256 $numReceivers;
    uint256 $amountPerReceiver;

    // Simulate a sender with enough balance to cover the batch transfer and a margin
    uint256 adjustedSenderBalance = $numReceivers * $amountPerReceiver + 500; // Adding a 500 unit margin
    balances[msg.sender] = adjustedSenderBalance;

    // Create a memory array of receiver addresses with symbolic length
    address[] memory simulatedReceivers = new address[]($numReceivers);

    // Compute the total expected amount to be transferred
    uint256 expectedTotalTransfer = $amountPerReceiver * $numReceivers;

    // Check that the sender's balance is sufficient for the expected transfer
    require(balances[msg.sender] >= expectedTotalTransfer, "Sender lacks sufficient balance");

    // Record the sender's balance before performing the batch transfer
    uint256 preTransferBalance = balances[msg.sender];

    // Execute the batch transfer simulation
    batchTransfer(simulatedReceivers, $amountPerReceiver);

    // Confirm the sender's balance decreases exactly by the expected transfer amount
    assert(balances[msg.sender] == preTransferBalance - expectedTotalTransfer);

    // Verify that each receiver gets the correct amount transferred
    for(uint i = 0; i < simulatedReceivers.length; i++) {
        // Assume each receiver starts with no balance
        uint256 initialReceiverBalance = 0;
        // Ensure each receiver's balance is increased by the precise transferred amount
        assert(balances[simulatedReceivers[i]] == initialReceiverBalance + $amountPerReceiver);
    }
}}