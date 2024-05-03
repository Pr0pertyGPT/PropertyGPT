// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IHummusRouter01 {
    function swapTokensForTokens(
        address[] calldata tokenPath,
        address[] calldata poolPath,
        uint256 fromAmount,
        uint256 minimumToAmount,
        address to,
        uint256 deadline
    ) external returns (uint256 amountOut, uint256 haircut);

    function quotePotentialSwaps(
        address[] calldata tokenPath,
        address[] calldata poolPath,
        uint256 fromAmount
    ) external view returns (uint256 potentialOutcome, uint256 haircut);
}
