// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import {HandlerBase} from "../HandlerBase.sol";
import {IHummusRouter01} from "./IHummusRouter01.sol";

contract HHummus is HandlerBase {
    // prettier-ignore
    IHummusRouter01 public immutable router;

    constructor(address router_) {
        router = IHummusRouter01(router_);
    }

    function getContractName() public pure override returns (string memory) {
        return "HHummus";
    }

    function swapTokensForTokens(
        uint256 fromAmount,
        uint256 minimumToAmount,
        address[] calldata tokenPath,
        address[] calldata poolPath
    ) external returns (uint256 amount) {
        address tokenIn = tokenPath[0];
        address tokenOut = tokenPath[tokenPath.length - 1];

        // Approve token
        fromAmount = _getBalance(tokenIn, fromAmount);
        _tokenApprove(tokenIn, address(router), fromAmount);

        try
            router.swapTokensForTokens(
                tokenPath,
                poolPath,
                fromAmount,
                minimumToAmount,
                address(this),
                block.timestamp
            )
        returns (uint256 amountOut, uint256) {
            amount = amountOut;
        } catch Error(string memory reason) {
            _revertMsg("swapTokensForTokens", reason);
        } catch {
            _revertMsg("swapTokensForTokens");
        }

        _tokenApproveZero(tokenIn, address(router));
        _updateToken(tokenOut);
    }
}
