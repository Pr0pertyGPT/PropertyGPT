// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IPredicate {
    event LockedEther(
        address indexed depositor,
        address indexed depositReceiver,
        uint256 amount
    );
    event LockedERC20(
        address indexed depositor,
        address indexed depositReceiver,
        address indexed rootToken,
        uint256 amount
    );
}
