pragma solidity 0.8.0;

contract VulnerableStaking{mapping(address => uint256) public balances;
uint256 public totalSupply;
function deposit(uint256) public   
precondition{}

postcondition{totalSupply == __old__(totalSupply) - amount;}
}