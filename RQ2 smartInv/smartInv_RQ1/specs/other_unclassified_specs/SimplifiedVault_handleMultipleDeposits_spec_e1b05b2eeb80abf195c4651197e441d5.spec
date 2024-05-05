pragma solidity 0.8.0;

contract SimplifiedVault {mapping(uint256 => FNFTConfig) public fnfts;
struct FNFTConfig {
        uint256 depositAmount;
    }

function handleMultipleDeposits(uint256,uint256,uint256) public  {}

rule ensureDepositNotDecreased() {
    uint256 $fnftId;
    uint256 $newFNFTId;
    uint256 $depositAmountBefore = fnfts[$fnftId].depositAmount;
    uint256 $amount;

    // Simulate the scenario where handleMultipleDeposits is called
    handleMultipleDeposits($fnftId, $newFNFTId, $amount);

    // Assert that the deposit amount has not decreased
    assert(fnfts[$fnftId].depositAmount >= $depositAmountBefore);
}}