// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

// Add handlers' event here for verify purpose in test
interface IHandlerEvents {
    // HPolygon
    event PolygonBridged(
        address indexed sender,
        address indexed token,
        uint256 amount
    );
}
