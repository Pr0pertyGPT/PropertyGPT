pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function removeLiquidity(uint256) public  {}

rule CheckRemoveLiquidity(){
    // Declare symbolic variables
    uint256 $liquidityToRemove;
    address $msgSenderAddress;

    // Store initial states
    uint256 initialLiquidityOfSender = liquidityBalance[$msgSenderAddress];
    uint256 initialBaseTokenReserve = baseTokenReserve;
    uint256 initialQuoteTokenReserve = quoteTokenReserve;
    uint256 initialTotalLiquidity = totalLiquidity;

    // Execute the function under test
    removeLiquidity($liquidityToRemove);

    // Compute expected outcomes
    uint256 expectedBaseTokenAmount = ($liquidityToRemove * initialBaseTokenReserve) / initialTotalLiquidity;
    uint256 expectedQuoteTokenAmount = ($liquidityToRemove * initialQuoteTokenReserve) / initialTotalLiquidity;

    // Assertions to validate post-execution state
    assert liquidityBalance[$msgSenderAddress] == initialLiquidityOfSender - $liquidityToRemove;
    assert baseTokenReserve == initialBaseTokenReserve - expectedBaseTokenAmount;
    assert quoteTokenReserve == initialQuoteTokenReserve - expectedQuoteTokenAmount;
    assert totalLiquidity == initialTotalLiquidity - $liquidityToRemove;
}}