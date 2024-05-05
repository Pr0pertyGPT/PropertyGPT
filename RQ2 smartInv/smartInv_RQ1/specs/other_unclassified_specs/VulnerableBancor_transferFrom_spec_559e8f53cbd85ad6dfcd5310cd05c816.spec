pragma solidity 0.8.0;

contract VulnerableBancor{mapping(address => mapping(address => uint256)) public allowance;
mapping(address => uint256) public balanceOf;
function transferFrom(address,address,uint256) public returns(bool) 
precondition{balanceOf[msg.sender] >= value; allowance[msg.sender][msg.sender] >= value;}

postcondition{__old__(balanceOf[msg.sender]) - value == balanceOf[msg.sender]; __old__(balanceOf[to]) + value == balanceOf[to]; __old__(allowance[msg.sender][msg.sender]) - value == allowance[msg.sender][msg.sender];}
}