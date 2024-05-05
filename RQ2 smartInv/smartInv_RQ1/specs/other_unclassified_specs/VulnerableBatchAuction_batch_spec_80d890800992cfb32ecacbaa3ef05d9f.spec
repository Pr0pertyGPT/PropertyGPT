pragma solidity 0.8.0;

contract VulnerableBatchAuction {uint256 public totalTokens;
mapping(address => uint256) public commitments;
uint256 public totalCommitments;


rule BatchCallsAllSucceed() {
    bytes[] memory $callData;
    uint256 $originalLength = $callData.length;
    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);

    uint256 $successfulCalls = 0;
    for (uint256 i = 0; i < $originalLength; i++) {
        (bool $callSuccess,) = address(this).delegatecall($callData[i]);
        if ($callSuccess) {
            $successfulCalls++;
        }
    }

    assert($successfulCalls == $originalLength);
}}