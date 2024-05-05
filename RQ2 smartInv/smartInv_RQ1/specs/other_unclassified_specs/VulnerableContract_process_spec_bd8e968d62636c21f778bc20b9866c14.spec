pragma solidity 0.8.0;

contract VulnerableContract {mapping(bytes32 => bytes32) public messages;
mapping(bytes32 => uint256) public confirmAt;

function acceptableRoot(bytes32) public returns(bool) {}
function process(bytes32) public  {}

rule verifyRootAcceptance() {
    bytes32 $messageHash;
    bool rootAcceptableBefore = acceptableRoot(messages[$messageHash]);
    process($messageHash);

    assert(rootAcceptableBefore);
}}