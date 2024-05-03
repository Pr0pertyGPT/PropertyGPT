// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;

interface ILayerZeroEndpoint{
    function estimateFees(uint16 _dstChainId, address _userApplication, bytes calldata _payload, bool _payInZRO, bytes calldata _adapterParams) external view returns (uint nativeFee, uint zroFee);
}
