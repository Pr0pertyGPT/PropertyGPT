// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface ISingletonFactory {
    function deploy(bytes calldata _initCode, bytes32 _salt) external returns (address payable createdContract);
}
