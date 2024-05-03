// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;


interface IStakingRewardsAdapterRegistry {
    function isValid(address handler) external view returns (bool result);
    function getInfo(address handler) external view returns (bytes32 info);
}
