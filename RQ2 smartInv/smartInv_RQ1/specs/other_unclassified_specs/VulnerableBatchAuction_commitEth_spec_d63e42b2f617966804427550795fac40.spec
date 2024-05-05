pragma solidity 0.8.0;

contract VulnerableBatchAuction{uint256 public totalTokens;
mapping(address => uint256) public commitments;
uint256 public totalCommitments;
function commitEth() public   
precondition{msg.value > 0}

postcondition{commitments[__old__(msg.sender)] + msg.value == commitments[msg.sender] ? __old__(totalCommitments) + msg.value == totalCommitments : true}
}