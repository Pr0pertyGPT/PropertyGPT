// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../HandlerBase.sol";

contract HParaSwapV5 is HandlerBase {
    using SafeERC20 for IERC20;

    // prettier-ignore
    address public constant AUGUSTUS_SWAPPER = 0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57;
    // prettier-ignore
    address public constant TOKEN_TRANSFER_PROXY = 0x216B4B4Ba9F3e719726886d34a177484278Bfcae;

    function getContractName() public pure override returns (string memory) {
        return "HParaSwapV5";
    }

    function swap(
        address srcToken,
        uint256 amount,
        address destToken,
        bytes calldata data
    ) external payable returns (uint256) {
        uint256 destTokenBalanceBefore = _getBalance(
            destToken,
            type(uint256).max
        );

        if (_isNotNativeToken(srcToken)) {
            // ERC20 token need to approve before paraswap
            _tokenApprove(srcToken, TOKEN_TRANSFER_PROXY, amount);
            _paraswapCall(0, data);
        } else {
            _paraswapCall(amount, data);
        }

        uint256 destTokenBalanceAfter = _getBalance(
            destToken,
            type(uint256).max
        );

        uint256 destTokenDelta = destTokenBalanceAfter - destTokenBalanceBefore;

        if (destTokenDelta == 0) {
            _revertMsg("swap", "Invalid output token amount");
        }

        if (_isNotNativeToken(destToken)) {
            _updateToken(destToken);
        }

        return destTokenDelta;
    }

    function _paraswapCall(uint256 value, bytes calldata data) internal {
        // Interact with paraswap through contract call with data
        (bool success, bytes memory returnData) = AUGUSTUS_SWAPPER.call{
            value: value
        }(data);

        if (!success) {
            if (returnData.length < 68) {
                // If the returnData length is less than 68, then the transaction failed silently.
                _revertMsg("_paraswapCall");
            } else {
                // Look for revert reason and bubble it up if present
                assembly {
                    returnData := add(returnData, 0x04)
                }
                _revertMsg("_paraswapCall", abi.decode(returnData, (string)));
            }
        }
    }
}
