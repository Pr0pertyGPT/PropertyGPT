pragma solidity 0.8.0;

contract SimplifiedLiquidityPool{mapping(address => mapping(address => uint256)) public liquidityBalance;
function removeLiquidity(address,address,uint256) public   
precondition{liquidityBalance[token][to] >= amount}

postcondition{liquidityBalance[token][to] == __old__(liquidityBalance[token][to]) - amount}
}