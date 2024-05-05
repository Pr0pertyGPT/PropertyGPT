pragma solidity 0.8.0;

contract SimplifiedLiquidityPool{mapping(address => mapping(address => uint256)) public liquidityBalance;
function addLiquidity(address,uint256) public   
precondition{}

postcondition{liquidityBalance[token][msg.sender] == __old__(liquidityBalance[token][msg.sender]) + amount;}
}