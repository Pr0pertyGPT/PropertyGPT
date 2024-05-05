pragma solidity 0.8.0;

contract SimpleCurve{mapping(address => uint256) public balances;
mapping(address => bool) public isBorrowed;
uint256 public totalLiquidity;
function flashLoan(uint256) public   
precondition{
    balances[address(this)] >= amount;
}

postcondition{
    balances[address(this)] == __old__(balances[address(this)]) - amount;
    isBorrowed[msg.sender] == false;
}
}