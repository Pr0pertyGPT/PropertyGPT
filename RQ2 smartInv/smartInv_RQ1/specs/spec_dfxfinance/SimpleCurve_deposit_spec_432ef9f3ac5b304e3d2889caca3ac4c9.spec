pragma solidity 0.8.0;

contract SimpleCurve{mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;
function deposit(uint256) public   
precondition{}

postcondition{balances[msg.sender] == __old__(balances[msg.sender]) + amount; balances[address(this)] == __old__(balances[address(this)]) + amount; totalLiquidity == __old__(totalLiquidity) + amount;}
}