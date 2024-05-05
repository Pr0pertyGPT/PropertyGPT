// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableBatchAuction {
    uint256 public totalTokens;
    mapping(address => uint256) public commitments;
    uint256 public totalCommitments;

    event CommitEth(address indexed sender, uint256 amount, uint256 totalCommitments);

    constructor(uint256 _totalTokens) {
        totalTokens = _totalTokens;
    }

    function commitEth() public payable {
        require(msg.value > 0, "You need to send some ether");
        commitments[msg.sender] += msg.value;
        totalCommitments += msg.value;
        emit CommitEth(msg.sender, msg.value, totalCommitments);
    }

    function batch(bytes[] calldata calls) public payable {
        for (uint256 i = 0; i < calls.length; i++) {
            (bool success, ) = address(this).delegatecall(calls[i]);
            require(success, "Batch call failed");
        }
    }

    function withdrawTokens() public {
        uint256 userCommitment = commitments[msg.sender];
        require(userCommitment > 0, "No commitments");
        uint256 tokenAmount = totalTokens * userCommitment / totalCommitments;
        commitments[msg.sender] = 0;  
        payable(msg.sender).transfer(userCommitment);  
        emit CommitEth(msg.sender, 0, totalCommitments);
    }
}
