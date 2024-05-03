// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import "../HandlerBase.sol";
import "../uniswapv2/libraries/UniswapV2Library.sol";
import "../uniswapv2/IUniswapV2Router02.sol";

contract HQuickSwap is HandlerBase {
    using SafeERC20 for IERC20;

    // prettier-ignore
    address public constant UNISWAPV2_ROUTER = 0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff;

    function getContractName() public pure override returns (string memory) {
        return "HQuickSwap";
    }

    function addLiquidityETH(
        uint256 value,
        address token,
        uint256 amountTokenDesired,
        uint256 amountTokenMin,
        uint256 amountETHMin
    )
        external
        payable
        returns (uint256 amountToken, uint256 amountETH, uint256 liquidity)
    {
        // Get uniswapV2 router
        IUniswapV2Router02 router = IUniswapV2Router02(UNISWAPV2_ROUTER);

        // Approve token
        value = _getBalance(address(0), value);
        amountTokenDesired = _getBalance(token, amountTokenDesired);
        _tokenApprove(token, UNISWAPV2_ROUTER, amountTokenDesired);

        // Add liquidity ETH
        try
            router.addLiquidityETH{value: value}(
                token,
                amountTokenDesired,
                amountTokenMin,
                amountETHMin,
                address(this),
                block.timestamp
            )
        returns (uint256 ret1, uint256 ret2, uint256 ret3) {
            amountToken = ret1;
            amountETH = ret2;
            liquidity = ret3;
        } catch Error(string memory reason) {
            _revertMsg("addLiquidityETH", reason);
        } catch {
            _revertMsg("addLiquidityETH");
        }
        _tokenApproveZero(token, UNISWAPV2_ROUTER);

        // Update involved token
        address pair = UniswapV2Library.pairFor(
            router.factory(),
            token,
            router.WETH()
        );
        _updateToken(pair);
    }

    function addLiquidity(
        address tokenA,
        address tokenB,
        uint256 amountADesired,
        uint256 amountBDesired,
        uint256 amountAMin,
        uint256 amountBMin
    )
        external
        payable
        returns (uint256 amountA, uint256 amountB, uint256 liquidity)
    {
        // Get uniswapV2 router
        IUniswapV2Router02 router = IUniswapV2Router02(UNISWAPV2_ROUTER);

        // Approve token
        amountADesired = _getBalance(tokenA, amountADesired);
        amountBDesired = _getBalance(tokenB, amountBDesired);
        _tokenApprove(tokenA, UNISWAPV2_ROUTER, amountADesired);
        _tokenApprove(tokenB, UNISWAPV2_ROUTER, amountBDesired);

        // Add liquidity
        try
            router.addLiquidity(
                tokenA,
                tokenB,
                amountADesired,
                amountBDesired,
                amountAMin,
                amountBMin,
                address(this),
                block.timestamp
            )
        returns (uint256 ret1, uint256 ret2, uint256 ret3) {
            amountA = ret1;
            amountB = ret2;
            liquidity = ret3;
        } catch Error(string memory reason) {
            _revertMsg("addLiquidity", reason);
        } catch {
            _revertMsg("addLiquidity");
        }
        _tokenApproveZero(tokenA, UNISWAPV2_ROUTER);
        _tokenApproveZero(tokenB, UNISWAPV2_ROUTER);

        // Update involved token
        address pair = UniswapV2Library.pairFor(
            router.factory(),
            tokenA,
            tokenB
        );
        _updateToken(pair);
    }

    function removeLiquidityETH(
        address token,
        uint256 liquidity,
        uint256 amountTokenMin,
        uint256 amountETHMin
    ) external payable returns (uint256 amountToken, uint256 amountETH) {
        // Get uniswapV2 router
        IUniswapV2Router02 router = IUniswapV2Router02(UNISWAPV2_ROUTER);
        address pair = UniswapV2Library.pairFor(
            router.factory(),
            token,
            router.WETH()
        );

        // Approve token
        liquidity = _getBalance(pair, liquidity);
        _tokenApprove(pair, UNISWAPV2_ROUTER, liquidity);

        // remove liquidityETH
        try
            router.removeLiquidityETH(
                token,
                liquidity,
                amountTokenMin,
                amountETHMin,
                address(this),
                block.timestamp
            )
        returns (uint256 ret1, uint256 ret2) {
            amountToken = ret1;
            amountETH = ret2;
        } catch Error(string memory reason) {
            _revertMsg("removeLiquidityETH", reason);
        } catch {
            _revertMsg("removeLiquidityETH");
        }
        _tokenApproveZero(pair, UNISWAPV2_ROUTER);

        // Update involved token
        _updateToken(token);
    }

    function removeLiquidity(
        address tokenA,
        address tokenB,
        uint256 liquidity,
        uint256 amountAMin,
        uint256 amountBMin
    ) external payable returns (uint256 amountA, uint256 amountB) {
        // Get uniswapV2 router
        IUniswapV2Router02 router = IUniswapV2Router02(UNISWAPV2_ROUTER);
        address pair = UniswapV2Library.pairFor(
            router.factory(),
            tokenA,
            tokenB
        );

        // Approve token
        liquidity = _getBalance(pair, liquidity);
        _tokenApprove(pair, UNISWAPV2_ROUTER, liquidity);

        // remove liquidity
        try
            router.removeLiquidity(
                tokenA,
                tokenB,
                liquidity,
                amountAMin,
                amountBMin,
                address(this),
                block.timestamp
            )
        returns (uint256 ret1, uint256 ret2) {
            amountA = ret1;
            amountB = ret2;
        } catch Error(string memory reason) {
            _revertMsg("removeLiquidity", reason);
        } catch {
            _revertMsg("removeLiquidity");
        }
        _tokenApproveZero(pair, UNISWAPV2_ROUTER);

        // Update involved token
        _updateToken(tokenA);
        _updateToken(tokenB);
    }

    function swapExactETHForTokens(
        uint256 value,
        uint256 amountOutMin,
        address[] calldata path
    ) external payable returns (uint256 amount) {
        _requireMsg(path.length >= 2, "swapExactETHForTokens", "invalid path");
        address tokenOut = path[path.length - 1];

        // Get uniswapV2 router
        IUniswapV2Router02 router = IUniswapV2Router02(UNISWAPV2_ROUTER);
        value = _getBalance(address(0), value);
        try
            router.swapExactETHForTokens{value: value}(
                amountOutMin,
                path,
                address(this),
                block.timestamp
            )
        returns (uint256[] memory amounts) {
            amount = amounts[amounts.length - 1];
        } catch Error(string memory reason) {
            _revertMsg("swapExactETHForTokens", reason);
        } catch {
            _revertMsg("swapExactETHForTokens");
        }

        _updateToken(tokenOut);
    }

    function swapETHForExactTokens(
        uint256 value,
        uint256 amountOut,
        address[] calldata path
    ) external payable returns (uint256 amount) {
        _requireMsg(path.length >= 2, "swapETHForExactTokens", "invalid path");
        address tokenOut = path[path.length - 1];

        // Get uniswapV2 router
        IUniswapV2Router02 router = IUniswapV2Router02(UNISWAPV2_ROUTER);

        // if amount == type(uint256).max return balance of Proxy
        value = _getBalance(address(0), value);

        try
            router.swapETHForExactTokens{value: value}(
                amountOut,
                path,
                address(this),
                block.timestamp
            )
        returns (uint256[] memory amounts) {
            amount = amounts[0];
        } catch Error(string memory reason) {
            _revertMsg("swapETHForExactTokens", reason);
        } catch {
            _revertMsg("swapETHForExactTokens");
        }

        _updateToken(tokenOut);
    }

    function swapExactTokensForETH(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path
    ) external payable returns (uint256 amount) {
        _requireMsg(path.length >= 2, "swapExactTokensForETH", "invalid path");
        address tokenIn = path[0];

        // Get uniswapV2 router
        IUniswapV2Router02 router = IUniswapV2Router02(UNISWAPV2_ROUTER);

        // Approve token
        amountIn = _getBalance(tokenIn, amountIn);
        _tokenApprove(tokenIn, UNISWAPV2_ROUTER, amountIn);

        try
            router.swapExactTokensForETH(
                amountIn,
                amountOutMin,
                path,
                address(this),
                block.timestamp
            )
        returns (uint256[] memory amounts) {
            amount = amounts[amounts.length - 1];
        } catch Error(string memory reason) {
            _revertMsg("swapExactTokensForETH", reason);
        } catch {
            _revertMsg("swapExactTokensForETH");
        }
        _tokenApproveZero(tokenIn, UNISWAPV2_ROUTER);
    }

    function swapTokensForExactETH(
        uint256 amountOut,
        uint256 amountInMax,
        address[] calldata path
    ) external payable returns (uint256 amount) {
        _requireMsg(path.length >= 2, "swapTokensForExactETH", "invalid path");
        address tokenIn = path[0];

        // Get uniswapV2 router
        IUniswapV2Router02 router = IUniswapV2Router02(UNISWAPV2_ROUTER);

        // if amount == type(uint256).max return balance of Proxy
        amountInMax = _getBalance(tokenIn, amountInMax);

        // Approve token
        _tokenApprove(tokenIn, UNISWAPV2_ROUTER, amountInMax);

        try
            router.swapTokensForExactETH(
                amountOut,
                amountInMax,
                path,
                address(this),
                block.timestamp
            )
        returns (uint256[] memory amounts) {
            amount = amounts[0];
        } catch Error(string memory reason) {
            _revertMsg("swapTokensForExactETH", reason);
        } catch {
            _revertMsg("swapTokensForExactETH");
        }
        _tokenApproveZero(tokenIn, UNISWAPV2_ROUTER);
    }

    function swapExactTokensForTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path
    ) external payable returns (uint256 amount) {
        _requireMsg(
            path.length >= 2,
            "swapExactTokensForTokens",
            "invalid path"
        );
        address tokenIn = path[0];
        address tokenOut = path[path.length - 1];

        // Get uniswapV2 router
        IUniswapV2Router02 router = IUniswapV2Router02(UNISWAPV2_ROUTER);

        // Approve token
        amountIn = _getBalance(tokenIn, amountIn);
        _tokenApprove(tokenIn, UNISWAPV2_ROUTER, amountIn);

        try
            router.swapExactTokensForTokens(
                amountIn,
                amountOutMin,
                path,
                address(this),
                block.timestamp
            )
        returns (uint256[] memory amounts) {
            amount = amounts[amounts.length - 1];
        } catch Error(string memory reason) {
            _revertMsg("swapExactTokensForTokens", reason);
        } catch {
            _revertMsg("swapExactTokensForTokens");
        }
        _tokenApproveZero(tokenIn, UNISWAPV2_ROUTER);

        _updateToken(tokenOut);
    }

    function swapTokensForExactTokens(
        uint256 amountOut,
        uint256 amountInMax,
        address[] calldata path
    ) external payable returns (uint256 amount) {
        _requireMsg(
            path.length >= 2,
            "swapTokensForExactTokens",
            "invalid path"
        );
        address tokenIn = path[0];
        address tokenOut = path[path.length - 1];

        // Get uniswapV2 router
        IUniswapV2Router02 router = IUniswapV2Router02(UNISWAPV2_ROUTER);

        // if amount == type(uint256).max return balance of Proxy
        amountInMax = _getBalance(tokenIn, amountInMax);

        // Approve token
        _tokenApprove(tokenIn, UNISWAPV2_ROUTER, amountInMax);

        try
            router.swapTokensForExactTokens(
                amountOut,
                amountInMax,
                path,
                address(this),
                block.timestamp
            )
        returns (uint256[] memory amounts) {
            amount = amounts[0];
        } catch Error(string memory reason) {
            _revertMsg("swapTokensForExactTokens", reason);
        } catch {
            _revertMsg("swapTokensForExactTokens");
        }
        _tokenApproveZero(tokenIn, UNISWAPV2_ROUTER);

        _updateToken(tokenOut);
    }
}
