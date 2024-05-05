// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./IMerkleRedeem.sol";

interface IStaking {
    function stakingToken() external view returns (address);
    function redeemable() external view returns (address);
    function stakeFor(address, uint256) external;
    function unstakeFor(address, uint256) external;
    function claimWeeks(address, IMerkleRedeem.Claim[] calldata) external;
}
