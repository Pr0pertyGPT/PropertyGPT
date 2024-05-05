// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

contract VulnerableContract {
    // Mapping of message hashes to their respective Merkle roots
    mapping(bytes32 => bytes32) public messages;
    // Mapping of roots to allowable confirmation times
    mapping(bytes32 => uint256) public confirmAt;

    // Event to log the processing of messages
    event MessageProcessed(bytes32 messageHash, bool success);

    // Simulated initialization function setting an incorrect default root
    function initialize() public {
        bytes32 defaultRoot = 0x0000000000000000000000000000000000000000000000000000000000000000;
        confirmAt[defaultRoot] = block.timestamp; // Incorrectly setting the default root as trusted
    }

    // Function to simulate the acceptance of a root based on a timer logic
    function acceptableRoot(bytes32 _root) public view returns (bool) {
        uint256 _time = confirmAt[_root];
        if (_time == 0) {
            return false;
        }
        return block.timestamp >= _time;
    }

    // Function to "process" a message if it has a valid root
    function process(bytes32 _messageHash) public {
        require(acceptableRoot(messages[_messageHash]), "Root not proven or acceptable");
        // Simulate successful message processing
        emit MessageProcessed(_messageHash, true);
    }

    // Function to "prove" a message and associate it with a root
    function prove(bytes32 _messageHash, bytes32 _root) public {
        require(_root != 0x0000000000000000000000000000000000000000000000000000000000000000, "Invalid root");
        // Simulate proving the message by recording its root
        messages[_messageHash] = _root;
    }
}
