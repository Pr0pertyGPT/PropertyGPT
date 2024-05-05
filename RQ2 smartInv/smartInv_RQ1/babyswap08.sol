// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableTokenSwap {
    struct TokenPair {
        address token1;
        address token2;
    }

    mapping(address => TokenPair) public tokenPairs;
    mapping(address => mapping(address => uint)) public balances;

    function swapExactTokensForTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address[] calldata factories
    ) external {
        require(path.length == factories.length + 1, "Invalid path and factories length");
        require(balances[msg.sender][path[0]] >= amountIn, "Insufficient balance");

        uint amountOut = amountIn; 

        for (uint i = 0; i < factories.length; i++) {
            TokenPair storage pair = tokenPairs[factories[i]];
            require(pair.token1 == path[i] && pair.token2 == path[i + 1], "Invalid token pair");

            balances[msg.sender][path[i]] -= amountIn;
            balances[msg.sender][path[i + 1]] += amountOut;
            amountIn = amountOut; 
        }

        require(balances[msg.sender][path[path.length - 1]] >= amountOutMin, "INSUFFICIENT_OUTPUT_AMOUNT");

        emit SwapCompleted(msg.sender, path[0], path[path.length - 1], amountOutMin, balances[msg.sender][path[path.length - 1]]);
    }

    function setFactoryTokenPair(address factory, address token1, address token2) external {
        tokenPairs[factory] = TokenPair(token1, token2);
    }

    function deposit(address token, uint amount) external {
        balances[msg.sender][token] += amount;
        emit Deposit(msg.sender, token, amount);
    }

    function withdraw(address token, uint amount) external {
        require(balances[msg.sender][token] >= amount, "Insufficient balance");
        balances[msg.sender][token] -= amount;
        emit Withdraw(msg.sender, token, amount);
    }

    event SwapCompleted(address indexed user, address tokenIn, address tokenOut, uint amountRequired, uint amountOut);
    event Deposit(address indexed user, address token, uint amount);
    event Withdraw(address indexed user, address token, uint amount);
}
