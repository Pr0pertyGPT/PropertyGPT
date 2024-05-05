// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./IAggregationExecutorV5.sol";

interface IAggregationRouterV5 {
    struct SwapDescriptionV5 {
        IERC20 srcToken;
        IERC20 dstToken;
        address payable srcReceiver;
        address payable dstReceiver;
        uint256 amount;
        uint256 minReturnAmount;
        uint256 flags;
    }

    function swap( //0x12aa3caf
        IAggregationExecutorV5 executor,
        SwapDescriptionV5 calldata desc,
        bytes calldata permit,
        bytes calldata data
    )
        external
        payable
        returns (
            uint256 returnAmount,
            uint256 spentAmount
        );

    function unoswap( //0x0502b1c5
        IERC20 srcToken,
        uint256 amount,
        uint256 minReturn,
        uint256[] calldata pools
    ) external payable returns (uint256 returnAmount);

    function uniswapV3Swap( //0xe449022e
        uint256 amount,
        uint256 minReturn,
        uint256[] calldata pools
    ) external payable returns (uint256 returnAmount);
}
