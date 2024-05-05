// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IDepositManager {
    event NewDepositBlock(address indexed owner, address indexed token, uint256 amountOrNFTId, uint256 depositBlockId);
    function depositERC20ForUser(address _token, address _user, uint256 _amount) external;
}
