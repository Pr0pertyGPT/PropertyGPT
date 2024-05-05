pragma solidity 0.8.0;

contract VulnerableTokenSwap {mapping(address => TokenPair) public tokenPairs;
mapping(address => mapping(address => uint)) public balances;
struct TokenPair {
        address token1;
        address token2;
    }

function swapExactTokensForTokens(uint256,uint256,address[],address[]) public  {}

rule EnsureValidPathAndFactoryLengths(){
    uint $amountIn;
    uint $amountOutMin;
    address[] memory $path = new address[](3);
    address[] memory $factories = new address[](2);

    swapExactTokensForTokens($amountIn, $amountOutMin, $path, $factories);

    assert($path.length == $factories.length + 1);
}}