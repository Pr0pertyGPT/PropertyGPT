pragma solidity 0.8.0;

contract SimpleElasticSwap {uint256 public baseTokenReserve;
uint256 public quoteTokenReserve;
mapping(address => uint256) public liquidityBalance;
uint256 public totalLiquidity;
uint256 public baseTokenTotalSupply = 100000;

function addLiquidity(uint256,uint256) public  {}

rule TestLiquidityAmountsForPositivity() {
    uint256 baseAmount;
    uint256 quoteAmount;
    // Assert that either baseAmount or quoteAmount being less than or equal to 0 should fail the require statement of addLiquidity
    if (baseAmount <= 0 || quoteAmount <= 0) {
        try this.addLiquidity(baseAmount, quoteAmount) {
            assert(false); // Should not reach here because addLiquidity should revert for non-positive amounts
        } catch {
            // This catch block is expected to execute due to the requirement violation in addLiquidity
        }
    }
}}