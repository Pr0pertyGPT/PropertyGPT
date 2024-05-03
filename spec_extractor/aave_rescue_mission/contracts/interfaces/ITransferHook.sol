// SPDX-License-Identifier: AGPL-3.0
pragma solidity >=0.7.0 <0.9.0;

interface ITransferHook {
    function onTransfer(address from, address to, uint256 amount) external;
}