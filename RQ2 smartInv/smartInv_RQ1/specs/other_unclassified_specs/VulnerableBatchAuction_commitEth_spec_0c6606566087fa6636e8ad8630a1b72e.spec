pragma solidity 0.8.0;

contract VulnerableBatchAuction {uint256 public totalTokens;
mapping(address => uint256) public commitments;
uint256 public totalCommitments;

function commitEth() public  {}

rule ensureCommitEthCorrectlyIncrementsTotalCommitments() {
    uint256 beforeTotalCommitments = totalCommitments;
    uint256 $msg_value = 1; // Set to a positive value to satisfy the function requirement

    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);
    __assume__(msg.value == $msg_value);

    commitEth();

    assert(totalCommitments == beforeTotalCommitments + $msg_value);
}}