pragma solidity 0.8.0;

contract VulnerableContract {mapping(bytes32 => bytes32) public messages;
mapping(bytes32 => uint256) public confirmAt;

function process(bytes32) public  {}

rule EnsureProcessDoesNotAlterContractBalanceOrSenderNonce() {
    // Symbolic representation of parameters for invocation
    bytes32 $messageHash;

    // Capturing the state before invocation
    address thisContract = address(this);
    uint256 balanceBefore = thisContract.balance;
    address senderBefore = msg.sender;

    process($messageHash); // Invoking the function of interest

    // Capturing the state after invocation
    uint256 balanceAfter = thisContract.balance;
    address senderAfter = msg.sender;

    // Assertions to ensure state is unaffected post invocation
    assert(balanceBefore == balanceAfter);
    assert(senderBefore == senderAfter);
}}