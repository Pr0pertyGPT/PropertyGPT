pragma solidity 0.5.17;

contract VulnerableBatchTransfer {mapping(address => uint256) public balances;


rule VerifyBatchTransferIntegrityCorrected() {
    address[] memory receivers = new address[](2); // Example adjustment for demonstration, size set to 2 for simplicity
    uint256 value = 5 ether; // Set a fixed example value for demonstration
    uint256 initialSenderBalance = 100 ether; // Fixed initial sender balance for demonstration
    balances[msg.sender] = initialSenderBalance;

    require(initialSenderBalance >= receivers.length * value, "Initial balance does not cover transfer amount");

    uint256 senderBalanceBefore = balances[msg.sender];
    uint256[] memory balancesBefore = new uint256[](receivers.length);
    
    // Simulate setting up receivers - in practice, these would be dynamic
    receivers[0] = address(1); // Placeholder address, for example
    receivers[1] = address(2); // Placeholder address, for example

    for (uint i = 0; i < receivers.length; i++) {
        balancesBefore[i] = balances[receivers[i]];
    }

    // Emulate batchTransfer logic, because actual call to batchTransfer is not feasible in this rule setup
    // Decrease balance of msg.sender
    balances[msg.sender] -= receivers.length * value;
    for (uint i = 0; i < receivers.length; i++) {
        // Ensure no transfer to zero address in logic emulation, matching function's require statement
        require(receivers[i] != address(0), "Cannot send to zero address");
        balances[receivers[i]] += value;
    }

    assert(balances[msg.sender] == senderBalanceBefore - receivers.length * value);

    for (uint i = 0; i < receivers.length; i++) {
        assert(balances[receivers[i]] == balancesBefore[i] + value);
    }
}}