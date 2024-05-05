pragma solidity 0.8.0;

contract VulnerableBancor{mapping(address => mapping(address => uint256)) public allowance;
mapping(address => uint256) public balanceOf;
function safeTransferFrom(address,address,address,uint256) public   
precondition{
balanceOf[_from] >= _value ? true : false; 
allowance[_from][msg.sender] >= _value ? true : false; 
}

postcondition{
__old__(balanceOf[_from]) - _value == balanceOf[_from] ? true : false; 
__old__(balanceOf[_to]) + _value == balanceOf[_to] ? true : false; 
}
}