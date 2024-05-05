pragma solidity 0.8.0;

contract VulnerableBatchAuction{uint256 public totalTokens;
mapping(address => uint256) public commitments;
uint256 public totalCommitments;
function commitEth() public   
precondition{msg.value > 0}

postcondition{commitments[msg.sender] == __old__(commitments[msg.sender]) + msg.value ? true : false; totalCommitments == __old__(totalCommitments) + msg.value ? true : false;}
}