// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

contract FeeCollectorMock {
    uint256 private sum;

    fallback() external payable {
        sum += 1;
    }
}
