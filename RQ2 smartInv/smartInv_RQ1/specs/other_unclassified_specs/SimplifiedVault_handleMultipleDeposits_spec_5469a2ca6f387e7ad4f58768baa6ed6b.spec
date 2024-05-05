pragma solidity 0.8.0;

contract SimplifiedVault {mapping(uint256 => FNFTConfig) public fnfts;
struct FNFTConfig {
        uint256 depositAmount;
    }

function handleMultipleDeposits(uint256,uint256,uint256) public  {}

rule HandleMultipleDepositsAssetUpdate() {
    uint256 $fnftId;
    uint256 $newFNFTId;
    uint256 $amount;
    uint256 depositAmountBefore = fnfts[$fnftId].depositAmount;
    uint256 newFNFTDepositAmountBefore;
    if($newFNFTId != 0) {
        newFNFTDepositAmountBefore = fnfts[$newFNFTId].depositAmount;
    }

    handleMultipleDeposits($fnftId, $newFNFTId, $amount);

    assert(fnfts[$fnftId].depositAmount == $amount);
    if($newFNFTId != 0) {
        assert(fnfts[$newFNFTId].depositAmount == $amount);
    } else {
        assert(newFNFTDepositAmountBefore == 0);
    }
}}