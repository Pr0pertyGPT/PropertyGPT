// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IMerkleRedeem {
    struct Claim {
        uint256 week;
        uint256 balance;
        bytes32[] merkleProof;
    }
    function token() external view returns (address);
    function claimWeeks(address, Claim[] calldata) external;
}
