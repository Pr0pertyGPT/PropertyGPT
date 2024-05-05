pragma solidity 0.8.0;

contract VulnerableTokenSwap {mapping(address => TokenPair) public tokenPairs;
mapping(address => mapping(address => uint)) public balances;
struct TokenPair {
        address token1;
        address token2;
    }


rule TestSwapExactTokensForTokens(){
    // Symbolic variables
    uint $amountIn;
    uint $amountOutMin;
    address[] memory $path;
    address[] memory $factories;
    address $sender;

    // Initial conditions
    uint $senderInitialBalance = balances[$sender][$path[0]];
    uint $amountOut = $amountIn; // Assume amount out is same as amount in for simplicity

    // Ensure the path and factories array length satisfy function requirements
    require($path.length == $factories.length + 1, "Invalid path and factories length");
    require(balances[$sender][$path[0]] >= $amountIn, "Insufficient balance");

    for (uint i = 0; i < $factories.length; i++) {
        // Validate the token pair from the current factory matches the path
        TokenPair storage pair = tokenPairs[$factories[i]];
        require(pair.token1 == $path[i] && pair.token2 == $path[i + 1], "Invalid token pair");

        // Simulate the balance update for swap
        balances[$sender][$path[i]] -= $amountIn;
        balances[$sender][$path[i + 1]] += $amountOut;
        
        // Prepare $amountIn for the next iteration
        $amountIn = $amountOut; 
    }

    // Ensure the final balance of the token at path end is greater or equal to $amountOutMin
    uint $senderFinalBalance = balances[$sender][$path[$path.length - 1]];
    assert($senderFinalBalance >= $amountOutMin);
}}