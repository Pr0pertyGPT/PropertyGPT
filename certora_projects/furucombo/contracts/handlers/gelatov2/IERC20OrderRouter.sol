// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IERC20OrderRouter {
    function depositToken(
        uint256 _amount,
        address _module,
        address _inputToken,
        address payable _owner,
        address _witness,
        bytes calldata _data,
        bytes32 _secret
    ) external;
}
