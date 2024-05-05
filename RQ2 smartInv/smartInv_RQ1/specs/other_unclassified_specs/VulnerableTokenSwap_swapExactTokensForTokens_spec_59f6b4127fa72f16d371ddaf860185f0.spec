pragma solidity 0.8.0;

contract VulnerableTokenSwap {mapping(address => TokenPair) public tokenPairs;
mapping(address => mapping(address => uint)) public balances;
struct TokenPair {
        address token1;
        address token2;
    }


rule VerifySwapExecution() {
    address[] memory path;
    address[] memory factories;
    uint256 amountIn;
    uint256 amountOutMin;
    address sender;

    // Validating the relationship between path and factories array sizes
    require(path.length == factories.length + 1);

    // Checking sender's balance for the first token in the path is sufficient
    require(balances[sender][path[0]] >= amountIn);

    uint256 currentAmountOut = amountIn;

    for (uint256 i = 0; i < factories.length; i++) {
        // Ensuring consecutive tokens in the swap path are correctly paired
        TokenPair storage currentPair = tokenPairs[factories[i]];
        require(currentPair.token1 == path[i] && currentPair.token2 == path[i + 1]);

        // Executing swap, adjusting sender's balances accordingly
        balances[sender][path[i]] -= amountIn;
        balances[sender][path[i + 1]] += currentAmountOut;

        // Updating amountIn for the next iteration to simulate continuous swaps
        amountIn = currentAmountOut;
    }

    // Verifying final token amount received meets or exceeds the minimum expectation
    assert(balances[sender][path[path.length - 1]] >= amountOutMin);
}}