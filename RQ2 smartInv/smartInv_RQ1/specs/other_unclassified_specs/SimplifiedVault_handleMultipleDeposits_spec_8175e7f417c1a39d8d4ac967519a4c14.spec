pragma solidity 0.8.0;

contract SimplifiedVault {mapping(uint256 => FNFTConfig) public fnfts;
struct FNFTConfig {
        uint256 depositAmount;
    }

function handleMultipleDeposits(uint256,uint256,uint256) public  {}

rule HandleMultipleDepositsDoesNotDecrease() {
    uint256 $fnftId;
    uint256 $newFNFTId;
    uint256 $amount;
    uint256 $depositAmount;

    fnfts[$fnftId].depositAmount = $depositAmount;
    
    uint256 depositAmountBefore = fnfts[$fnftId].depositAmount;
    
    handleMultipleDeposits($fnftId, $newFNFTId, $amount);
    
    assert(fnfts[$fnftId].depositAmount >= depositAmountBefore);
}}