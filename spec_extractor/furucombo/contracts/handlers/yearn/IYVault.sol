// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IYVault {
    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount)
        external
        returns (bool);

    function token() external view returns (address);

    function getPricePerFullShare() external view returns (uint256);

    function deposit(uint256 _amount) external;

    function depositETH() external payable;

    function withdraw(uint256 _shares) external;

    function withdrawETH(uint256 _shares) external;
}
