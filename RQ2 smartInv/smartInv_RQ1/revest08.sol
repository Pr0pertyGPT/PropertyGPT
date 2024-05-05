// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract SimplifiedVault {
    struct FNFTConfig {
        uint256 depositAmount;
    }

    mapping(uint256 => FNFTConfig) public fnfts;

    function createFNFT(uint256 fnftId, uint256 initialDeposit) public {
        fnfts[fnftId] = FNFTConfig(initialDeposit);
    }

    function handleMultipleDeposits(
        uint256 fnftId,
        uint256 newFNFTId,
        uint256 amount
    ) public {
        require(amount >= fnfts[fnftId].depositAmount, "Deposit must not decrease");

        fnfts[fnftId].depositAmount = amount;

        if (newFNFTId != 0) {
            fnfts[newFNFTId] = FNFTConfig(amount);
        }
    }

    function getDepositAmount(uint256 fnftId) public view returns (uint256) {
        return fnfts[fnftId].depositAmount;
    }
}
