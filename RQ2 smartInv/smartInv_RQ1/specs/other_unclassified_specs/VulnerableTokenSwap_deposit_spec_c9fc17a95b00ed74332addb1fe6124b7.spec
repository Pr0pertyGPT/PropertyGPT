pragma solidity 0.8.0;

contract VulnerableTokenSwap{mapping(address => TokenPair) public tokenPairs;
mapping(address => mapping(address => uint)) public balances;
struct TokenPair {
        address token1;
        address token2;
    }
function deposit(address,uint256) public   
precondition{}

postcondition{balances[msg.sender][token] == __old__(balances[msg.sender][token]) + amount;}
}