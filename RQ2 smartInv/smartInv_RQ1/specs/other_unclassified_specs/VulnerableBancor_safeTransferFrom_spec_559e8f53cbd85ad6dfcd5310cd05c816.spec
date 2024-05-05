pragma solidity 0.8.0;

contract VulnerableBancor{mapping(address => mapping(address => uint256)) public allowance;
mapping(address => uint256) public balanceOf;
function safeTransferFrom(address,address,address,uint256) public   
precondition{}

postcondition{
    balanceOf[_from] == __old__(balanceOf[_from]) - _value;
    balanceOf[_to] == __old__(balanceOf[_to]) + _value;
}
}