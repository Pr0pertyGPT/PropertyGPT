// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract ActionsMock {
    function approveToken(address token, address to, uint256 amount) external {
        IERC20(token).approve(to, amount);
    }
}
