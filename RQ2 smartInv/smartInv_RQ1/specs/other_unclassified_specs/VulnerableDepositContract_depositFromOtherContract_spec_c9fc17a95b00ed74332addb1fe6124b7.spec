pragma solidity 0.8.0;

contract VulnerableDepositContract{mapping(address => uint256) public deposits;
function depositFromOtherContract(uint256,address) public   
precondition{}

postcondition{deposits[_forAddress] == __old__(deposits[_forAddress]) + _depositAmount;}
}