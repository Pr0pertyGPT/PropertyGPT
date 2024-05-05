pragma solidity 0.8.0;

contract VulnerableReserve{mapping(address => uint256) public balances;
mapping(address => uint256) public debts;
uint256 public totalReserve;
function donateToReserves(uint256) public   
precondition{balances[msg.sender] >= amount}

postcondition{balances[msg.sender] == __old__(balances[msg.sender]) - amount ? totalReserve == __old__(totalReserve) + amount : true}
}