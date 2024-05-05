pragma solidity 0.8.0;

contract VulnerableContract {mapping(bytes32 => bytes32) public messages;
mapping(bytes32 => uint256) public confirmAt;

function process(bytes32) public  {}

rule ValidateAndProcessMessage() {
    bytes32 $messageHash;
    bool $messageValidity;

    if ($messageValidity) {
        // Directly call the process function since 'try' cannot be used with non-external functions
        process($messageHash);
        // If the process function executes without reverting, it's considered successful for valid messages
    } else {
        bool didProcessingFail = false;
        
        try this.process($messageHash) {
            // If the process function does not revert, it means processing an invalid message succeeded unexpectedly
        } catch {
            // If an error is caught, it means processing an invalid message failed as expected
            didProcessingFail = true;
        }

        // Assert that processing of invalid messages should indeed fail
        assert(didProcessingFail);
    }
}}