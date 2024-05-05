pragma solidity 0.8.0;

contract VulnerableContract{mapping(bytes32 => bytes32) public messages;
mapping(bytes32 => uint256) public confirmAt;
function process(bytes32) public   
precondition{}

postcondition{}
}