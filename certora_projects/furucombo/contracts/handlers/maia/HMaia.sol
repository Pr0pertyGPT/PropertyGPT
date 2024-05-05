// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import "./IV3SwapRouter.sol";
import "../HandlerBase.sol";
import "../uniswapv3/libraries/BytesLib.sol";

contract HMaia is HandlerBase {
    using SafeERC20 for IERC20;
    using BytesLib for bytes;

    // prettier-ignore
    IV3SwapRouter public constant ROUTER = IV3SwapRouter(0x07Da720AD5E434971dbe77C7fC85b7b44d5aC704);

    uint256 private constant PATH_SIZE = 43; // address + address + uint24
    uint256 private constant ADDRESS_SIZE = 20;

    function getContractName() public pure override returns (string memory) {
        return "HMaia";
    }

    function exactInputSingle(
        address tokenIn,
        address tokenOut,
        uint24 fee,
        uint256 amountIn,
        uint256 amountOutMinimum,
        uint160 sqrtPriceLimitX96
    ) external payable returns (uint256 amountOut) {
        // Build params for router call
        IV3SwapRouter.ExactInputSingleParams memory params;
        params.tokenIn = tokenIn;
        params.tokenOut = tokenOut;
        params.fee = fee;
        params.amountIn = _getBalance(tokenIn, amountIn);
        params.amountOutMinimum = amountOutMinimum;
        params.sqrtPriceLimitX96 = sqrtPriceLimitX96;

        // Approve token
        _tokenApprove(tokenIn, address(ROUTER), params.amountIn);
        amountOut = _exactInputSingle(0, params);
        _tokenApproveZero(tokenIn, address(ROUTER));
        _updateToken(tokenOut);
    }

    function exactInput(
        bytes memory path,
        uint256 amountIn,
        uint256 amountOutMinimum
    ) external payable returns (uint256 amountOut) {
        // Extract tokenIn and tokenOut
        address tokenIn = _getFirstToken(path);
        address tokenOut = _getLastToken(path);
        // Build params for router call
        IV3SwapRouter.ExactInputParams memory params;
        params.path = path;
        params.amountIn = _getBalance(tokenIn, amountIn);
        params.amountOutMinimum = amountOutMinimum;

        // Approve token
        _tokenApprove(tokenIn, address(ROUTER), params.amountIn);
        amountOut = _exactInput(0, params);
        _tokenApproveZero(tokenIn, address(ROUTER));
        _updateToken(tokenOut);
    }

    function exactOutputSingle(
        address tokenIn,
        address tokenOut,
        uint24 fee,
        uint256 amountOut,
        uint256 amountInMaximum,
        uint160 sqrtPriceLimitX96
    ) external payable returns (uint256 amountIn) {
        // Build params for router call
        IV3SwapRouter.ExactOutputSingleParams memory params;
        params.tokenIn = tokenIn;
        params.tokenOut = tokenOut;
        params.fee = fee;
        params.amountOut = amountOut;
        // if amount == type(uint256).max return balance of Proxy
        params.amountInMaximum = _getBalance(tokenIn, amountInMaximum);
        params.sqrtPriceLimitX96 = sqrtPriceLimitX96;

        // Approve token
        _tokenApprove(params.tokenIn, address(ROUTER), params.amountInMaximum);
        amountIn = _exactOutputSingle(0, params);
        _tokenApproveZero(params.tokenIn, address(ROUTER));
        _updateToken(params.tokenOut);
    }

    function exactOutput(
        bytes memory path,
        uint256 amountOut,
        uint256 amountInMaximum
    ) external payable returns (uint256 amountIn) {
        // Extract tokenIn and tokenOut
        // Note that the first token is tokenOut in exactOutput functions, vice versa
        address tokenIn = _getLastToken(path);
        address tokenOut = _getFirstToken(path);
        // Build params for router call
        IV3SwapRouter.ExactOutputParams memory params;
        params.path = path;
        params.amountOut = amountOut;
        // if amount == type(uint256).max return balance of Proxy
        params.amountInMaximum = _getBalance(tokenIn, amountInMaximum);

        // Approve token
        _tokenApprove(tokenIn, address(ROUTER), params.amountInMaximum);
        amountIn = _exactOutput(0, params);
        _tokenApproveZero(tokenIn, address(ROUTER));
        _updateToken(tokenOut);
    }

    function _getFirstToken(bytes memory path) internal pure returns (address) {
        return path.toAddress(0);
    }

    function _getLastToken(bytes memory path) internal pure returns (address) {
        _requireMsg(path.length >= PATH_SIZE, "General", "Path size too small");
        return path.toAddress(path.length - ADDRESS_SIZE);
    }

    function _exactInputSingle(
        uint256 value,
        IV3SwapRouter.ExactInputSingleParams memory params
    ) internal returns (uint256) {
        params.recipient = address(this);

        try ROUTER.exactInputSingle{value: value}(params) returns (
            uint256 amountOut
        ) {
            return amountOut;
        } catch Error(string memory reason) {
            _revertMsg("exactInputSingle", reason);
        } catch {
            _revertMsg("exactInputSingle");
        }
    }

    function _exactInput(
        uint256 value,
        IV3SwapRouter.ExactInputParams memory params
    ) internal returns (uint256) {
        params.recipient = address(this);

        try ROUTER.exactInput{value: value}(params) returns (
            uint256 amountOut
        ) {
            return amountOut;
        } catch Error(string memory reason) {
            _revertMsg("exactInput", reason);
        } catch {
            _revertMsg("exactInput");
        }
    }

    function _exactOutputSingle(
        uint256 value,
        IV3SwapRouter.ExactOutputSingleParams memory params
    ) internal returns (uint256) {
        params.recipient = address(this);

        try ROUTER.exactOutputSingle{value: value}(params) returns (
            uint256 amountIn
        ) {
            return amountIn;
        } catch Error(string memory reason) {
            _revertMsg("exactOutputSingle", reason);
        } catch {
            _revertMsg("exactOutputSingle");
        }
    }

    function _exactOutput(
        uint256 value,
        IV3SwapRouter.ExactOutputParams memory params
    ) internal returns (uint256) {
        params.recipient = address(this);

        try ROUTER.exactOutput{value: value}(params) returns (
            uint256 amountIn
        ) {
            return amountIn;
        } catch Error(string memory reason) {
            _revertMsg("exactOutput", reason);
        } catch {
            _revertMsg("exactOutput");
        }
    }
}
