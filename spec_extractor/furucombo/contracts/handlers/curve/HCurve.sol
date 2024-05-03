// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../HandlerBase.sol";
import "./ICurveHandler.sol";

contract HCurve is HandlerBase {
    using SafeERC20 for IERC20;

    function getContractName() public pure override returns (string memory) {
        return "HCurve";
    }

    /// @notice Curve exchange
    function exchange(
        address handler,
        address tokenI,
        address tokenJ,
        int128 i,
        int128 j,
        uint256 amount,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _amount,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _exchangeBefore(handler, tokenI, tokenJ, amount);
        try
            ICurveHandler(handler).exchange{value: ethAmount}(
                i,
                j,
                _amount,
                minAmount
            )
        {} catch Error(string memory reason) {
            _revertMsg("exchange", reason);
        } catch {
            _revertMsg("exchange");
        }

        return _exchangeAfter(handler, tokenI, tokenJ, balanceBefore);
    }

    /// @notice Curve exchange with uint256 ij
    function exchangeUint256(
        address handler,
        address tokenI,
        address tokenJ,
        uint256 i,
        uint256 j,
        uint256 amount,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _amount,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _exchangeBefore(handler, tokenI, tokenJ, amount);
        try
            ICurveHandler(handler).exchange{value: ethAmount}(
                i,
                j,
                _amount,
                minAmount
            )
        {} catch Error(string memory reason) {
            _revertMsg("exchangeUint256", reason);
        } catch {
            _revertMsg("exchangeUint256");
        }

        return _exchangeAfter(handler, tokenI, tokenJ, balanceBefore);
    }

    /// @notice Curve exchange with uint256 ij and ether flag
    function exchangeUint256Ether(
        address handler,
        address tokenI,
        address tokenJ,
        uint256 i,
        uint256 j,
        uint256 amount,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _amount,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _exchangeBefore(handler, tokenI, tokenJ, amount);
        try
            ICurveHandler(handler).exchange{value: ethAmount}(
                i,
                j,
                _amount,
                minAmount,
                true
            )
        {} catch Error(string memory reason) {
            _revertMsg("exchangeUint256Ether", reason);
        } catch {
            _revertMsg("exchangeUint256Ether");
        }

        return _exchangeAfter(handler, tokenI, tokenJ, balanceBefore);
    }

    /// @notice Curve exchange underlying
    function exchangeUnderlying(
        address handler,
        address tokenI,
        address tokenJ,
        int128 i,
        int128 j,
        uint256 amount,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _amount,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _exchangeBefore(handler, tokenI, tokenJ, amount);
        try
            ICurveHandler(handler).exchange_underlying{value: ethAmount}(
                i,
                j,
                _amount,
                minAmount
            )
        {} catch Error(string memory reason) {
            _revertMsg("exchangeUnderlying", reason);
        } catch {
            _revertMsg("exchangeUnderlying");
        }

        return _exchangeAfter(handler, tokenI, tokenJ, balanceBefore);
    }

    /// @notice Curve exchange underlying with factory zap
    function exchangeUnderlyingFactoryZap(
        address handler,
        address pool,
        address tokenI,
        address tokenJ,
        int128 i,
        int128 j,
        uint256 amount,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _amount,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _exchangeBefore(handler, tokenI, tokenJ, amount);
        try
            ICurveHandler(handler).exchange_underlying{value: ethAmount}(
                pool,
                i,
                j,
                _amount,
                minAmount
            )
        {} catch Error(string memory reason) {
            _revertMsg("exchangeUnderlyingFactoryZap", reason);
        } catch {
            _revertMsg("exchangeUnderlyingFactoryZap");
        }

        return _exchangeAfter(handler, tokenI, tokenJ, balanceBefore);
    }

    /// @notice Curve exchange underlying with uint256 ij
    function exchangeUnderlyingUint256(
        address handler,
        address tokenI,
        address tokenJ,
        uint256 i,
        uint256 j,
        uint256 amount,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _amount,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _exchangeBefore(handler, tokenI, tokenJ, amount);
        try
            ICurveHandler(handler).exchange_underlying{value: ethAmount}(
                i,
                j,
                _amount,
                minAmount
            )
        {} catch Error(string memory reason) {
            _revertMsg("exchangeUnderlyingUint256", reason);
        } catch {
            _revertMsg("exchangeUnderlyingUint256");
        }

        return _exchangeAfter(handler, tokenI, tokenJ, balanceBefore);
    }

    function _exchangeBefore(
        address handler,
        address tokenI,
        address tokenJ,
        uint256 amount
    ) internal returns (uint256, uint256, uint256) {
        amount = _getBalance(tokenI, amount);
        uint256 balanceBefore = _getBalance(tokenJ, type(uint256).max);

        // Approve erc20 token or set eth amount
        uint256 ethAmount;
        if (tokenI != NATIVE_TOKEN_ADDRESS) {
            _tokenApprove(tokenI, handler, amount);
        } else {
            ethAmount = amount;
        }

        return (amount, balanceBefore, ethAmount);
    }

    function _exchangeAfter(
        address handler,
        address tokenI,
        address tokenJ,
        uint256 balanceBefore
    ) internal returns (uint256) {
        uint256 balance = _getBalance(tokenJ, type(uint256).max);
        _requireMsg(
            balance > balanceBefore,
            "_exchangeAfter",
            "after <= before"
        );

        if (tokenI != NATIVE_TOKEN_ADDRESS) _tokenApproveZero(tokenI, handler);

        if (tokenJ != NATIVE_TOKEN_ADDRESS) _updateToken(tokenJ);

        return balance - balanceBefore;
    }

    /// @notice Curve add liquidity
    function addLiquidity(
        address handler,
        address pool,
        address[] calldata tokens,
        uint256[] calldata amounts,
        uint256 minPoolAmount
    ) external payable returns (uint256) {
        (
            uint256[] memory _amounts,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _addLiquidityBefore(handler, pool, tokens, amounts);

        // Execute add_liquidity according to amount array size
        if (_amounts.length == 2) {
            uint256[2] memory amts = [_amounts[0], _amounts[1]];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidity", reason);
            } catch {
                _revertMsg("addLiquidity");
            }
        } else if (_amounts.length == 3) {
            uint256[3] memory amts = [_amounts[0], _amounts[1], _amounts[2]];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidity", reason);
            } catch {
                _revertMsg("addLiquidity");
            }
        } else if (_amounts.length == 4) {
            uint256[4] memory amts = [
                _amounts[0],
                _amounts[1],
                _amounts[2],
                _amounts[3]
            ];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidity", reason);
            } catch {
                _revertMsg("addLiquidity");
            }
        } else if (_amounts.length == 5) {
            uint256[5] memory amts = [
                _amounts[0],
                _amounts[1],
                _amounts[2],
                _amounts[3],
                _amounts[4]
            ];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidity", reason);
            } catch {
                _revertMsg("addLiquidity");
            }
        } else if (_amounts.length == 6) {
            uint256[6] memory amts = [
                _amounts[0],
                _amounts[1],
                _amounts[2],
                _amounts[3],
                _amounts[4],
                _amounts[5]
            ];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidity", reason);
            } catch {
                _revertMsg("addLiquidity");
            }
        } else {
            _revertMsg("addLiquidity", "invalid amount[] size");
        }

        return
            _addLiquidityAfter(handler, pool, tokens, amounts, balanceBefore);
    }

    /// @notice Curve add liquidity with underlying true flag
    function addLiquidityUnderlying(
        address handler,
        address pool,
        address[] calldata tokens,
        uint256[] calldata amounts,
        uint256 minPoolAmount
    ) external payable returns (uint256) {
        (
            uint256[] memory _amounts,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _addLiquidityBefore(handler, pool, tokens, amounts);

        // Execute add_liquidity according to amount array size
        if (_amounts.length == 2) {
            uint256[2] memory amts = [_amounts[0], _amounts[1]];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount,
                    true
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidityUnderlying", reason);
            } catch {
                _revertMsg("addLiquidityUnderlying");
            }
        } else if (_amounts.length == 3) {
            uint256[3] memory amts = [_amounts[0], _amounts[1], _amounts[2]];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount,
                    true
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidityUnderlying", reason);
            } catch {
                _revertMsg("addLiquidityUnderlying");
            }
        } else if (_amounts.length == 4) {
            uint256[4] memory amts = [
                _amounts[0],
                _amounts[1],
                _amounts[2],
                _amounts[3]
            ];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount,
                    true
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidityUnderlying", reason);
            } catch {
                _revertMsg("addLiquidityUnderlying");
            }
        } else if (_amounts.length == 5) {
            uint256[5] memory amts = [
                _amounts[0],
                _amounts[1],
                _amounts[2],
                _amounts[3],
                _amounts[4]
            ];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount,
                    true
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidityUnderlying", reason);
            } catch {
                _revertMsg("addLiquidityUnderlying");
            }
        } else if (_amounts.length == 6) {
            uint256[6] memory amts = [
                _amounts[0],
                _amounts[1],
                _amounts[2],
                _amounts[3],
                _amounts[4],
                _amounts[5]
            ];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    amts,
                    minPoolAmount,
                    true
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidityUnderlying", reason);
            } catch {
                _revertMsg("addLiquidityUnderlying");
            }
        } else {
            _revertMsg("addLiquidityUnderlying", "invalid amount[] size");
        }

        return
            _addLiquidityAfter(handler, pool, tokens, amounts, balanceBefore);
    }

    /// @notice Curve add liquidity with factory zap
    function addLiquidityFactoryZap(
        address handler,
        address pool,
        address[] calldata tokens,
        uint256[] calldata amounts,
        uint256 minPoolAmount
    ) external payable returns (uint256) {
        (
            uint256[] memory _amounts,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _addLiquidityBefore(handler, pool, tokens, amounts);

        // Execute add_liquidity according to amount array size
        if (_amounts.length == 3) {
            uint256[3] memory amts = [_amounts[0], _amounts[1], _amounts[2]];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    pool,
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidityFactoryZap", reason);
            } catch {
                _revertMsg("addLiquidityFactoryZap");
            }
        } else if (_amounts.length == 4) {
            uint256[4] memory amts = [
                _amounts[0],
                _amounts[1],
                _amounts[2],
                _amounts[3]
            ];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    pool,
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidityFactoryZap", reason);
            } catch {
                _revertMsg("addLiquidityFactoryZap");
            }
        } else if (_amounts.length == 5) {
            uint256[5] memory amts = [
                _amounts[0],
                _amounts[1],
                _amounts[2],
                _amounts[3],
                _amounts[4]
            ];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    pool,
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidityFactoryZap", reason);
            } catch {
                _revertMsg("addLiquidityFactoryZap");
            }
        } else if (_amounts.length == 6) {
            uint256[6] memory amts = [
                _amounts[0],
                _amounts[1],
                _amounts[2],
                _amounts[3],
                _amounts[4],
                _amounts[5]
            ];
            try
                ICurveHandler(handler).add_liquidity{value: ethAmount}(
                    pool,
                    amts,
                    minPoolAmount
                )
            {} catch Error(string memory reason) {
                _revertMsg("addLiquidityFactoryZap", reason);
            } catch {
                _revertMsg("addLiquidityFactoryZap");
            }
        } else {
            _revertMsg("addLiquidityFactoryZap", "invalid amount[] size");
        }

        return
            _addLiquidityAfter(handler, pool, tokens, amounts, balanceBefore);
    }

    function _addLiquidityBefore(
        address handler,
        address pool,
        address[] memory tokens,
        uint256[] memory amounts
    ) internal returns (uint256[] memory, uint256, uint256) {
        uint256 balanceBefore = IERC20(pool).balanceOf(address(this));

        // Approve non-zero amount erc20 token and set eth amount
        uint256 ethAmount;
        for (uint256 i = 0; i < amounts.length; i++) {
            if (amounts[i] == 0) continue;
            amounts[i] = _getBalance(tokens[i], amounts[i]);
            if (tokens[i] == NATIVE_TOKEN_ADDRESS) {
                ethAmount = amounts[i];
                continue;
            }
            _tokenApprove(tokens[i], handler, amounts[i]);
        }

        return (amounts, balanceBefore, ethAmount);
    }

    function _addLiquidityAfter(
        address handler,
        address pool,
        address[] memory tokens,
        uint256[] memory amounts,
        uint256 balanceBefore
    ) internal returns (uint256) {
        uint256 balance = IERC20(pool).balanceOf(address(this));
        _requireMsg(
            balance > balanceBefore,
            "_addLiquidityAfter",
            "after <= before"
        );

        for (uint256 i = 0; i < amounts.length; i++) {
            if (amounts[i] == 0) continue;
            if (tokens[i] != NATIVE_TOKEN_ADDRESS)
                _tokenApproveZero(tokens[i], handler);
        }

        // Update post process
        _updateToken(address(pool));

        return balance - balanceBefore;
    }

    /// @notice Curve remove liquidity one coin
    function removeLiquidityOneCoin(
        address handler,
        address pool,
        address tokenI,
        uint256 poolAmount,
        int128 i,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _poolAmount,
            uint256 balanceBefore
        ) = _removeLiquidityOneCoinBefore(handler, pool, tokenI, poolAmount);
        try
            ICurveHandler(handler).remove_liquidity_one_coin(
                _poolAmount,
                i,
                minAmount
            )
        {} catch Error(string memory reason) {
            _revertMsg("removeLiquidityOneCoin", reason);
        } catch {
            _revertMsg("removeLiquidityOneCoin");
        }

        return
            _removeLiquidityOneCoinAfter(handler, pool, tokenI, balanceBefore);
    }

    /// @notice Curve remove liquidity one coin with uint256 i
    function removeLiquidityOneCoinUint256(
        address handler,
        address pool,
        address tokenI,
        uint256 poolAmount,
        uint256 i,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _poolAmount,
            uint256 balanceBefore
        ) = _removeLiquidityOneCoinBefore(handler, pool, tokenI, poolAmount);
        try
            ICurveHandler(handler).remove_liquidity_one_coin(
                _poolAmount,
                i,
                minAmount
            )
        {} catch Error(string memory reason) {
            _revertMsg("removeLiquidityOneCoinUint256", reason);
        } catch {
            _revertMsg("removeLiquidityOneCoinUint256");
        }

        return
            _removeLiquidityOneCoinAfter(handler, pool, tokenI, balanceBefore);
    }

    /// @notice Curve remove liquidity one coin underlying
    function removeLiquidityOneCoinUnderlying(
        address handler,
        address pool,
        address tokenI,
        uint256 poolAmount,
        int128 i,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _poolAmount,
            uint256 balanceBefore
        ) = _removeLiquidityOneCoinBefore(handler, pool, tokenI, poolAmount);
        try
            ICurveHandler(handler).remove_liquidity_one_coin(
                _poolAmount,
                i,
                minAmount,
                true
            )
        {} catch Error(string memory reason) {
            _revertMsg("removeLiquidityOneCoinUnderlying", reason);
        } catch {
            _revertMsg("removeLiquidityOneCoinUnderlying");
        }

        return
            _removeLiquidityOneCoinAfter(handler, pool, tokenI, balanceBefore);
    }

    /// @notice Curve remove liquidity one coin underlying with uint256 i
    function removeLiquidityOneCoinUnderlyingUint256(
        address handler,
        address pool,
        address tokenI,
        uint256 poolAmount,
        uint256 i,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _poolAmount,
            uint256 balanceBefore
        ) = _removeLiquidityOneCoinBefore(handler, pool, tokenI, poolAmount);
        try
            ICurveHandler(handler).remove_liquidity_one_coin(
                _poolAmount,
                i,
                minAmount,
                true
            )
        {} catch Error(string memory reason) {
            _revertMsg("removeLiquidityOneCoinUnderlyingUint256", reason);
        } catch {
            _revertMsg("removeLiquidityOneCoinUnderlyingUint256");
        }

        return
            _removeLiquidityOneCoinAfter(handler, pool, tokenI, balanceBefore);
    }

    /// @notice Curve remove liquidity one coin with with factory zap
    function removeLiquidityOneCoinFactoryZap(
        address handler,
        address pool,
        address tokenI,
        uint256 poolAmount,
        int128 i,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _poolAmount,
            uint256 balanceBefore
        ) = _removeLiquidityOneCoinBefore(handler, pool, tokenI, poolAmount);
        try
            ICurveHandler(handler).remove_liquidity_one_coin(
                pool,
                _poolAmount,
                i,
                minAmount
            )
        {} catch Error(string memory reason) {
            _revertMsg("removeLiquidityOneCoinFactoryZap", reason);
        } catch {
            _revertMsg("removeLiquidityOneCoinFactoryZap");
        }

        return
            _removeLiquidityOneCoinAfter(handler, pool, tokenI, balanceBefore);
    }

    function _removeLiquidityOneCoinBefore(
        address handler,
        address pool,
        address tokenI,
        uint256 poolAmount
    ) internal returns (uint256, uint256) {
        uint256 balanceBefore = _getBalance(tokenI, type(uint256).max);
        poolAmount = _getBalance(pool, poolAmount);
        _tokenApprove(pool, handler, poolAmount);

        return (poolAmount, balanceBefore);
    }

    function _removeLiquidityOneCoinAfter(
        address handler,
        address pool,
        address tokenI,
        uint256 balanceBefore
    ) internal returns (uint256) {
        // Some curve non-underlying pools like 3pool won't consume pool token
        // allowance since pool token was issued by the pool that don't need to
        // call transferFrom(). So set approval to 0 here.
        _tokenApproveZero(pool, handler);
        uint256 balance = _getBalance(tokenI, type(uint256).max);
        _requireMsg(
            balance > balanceBefore,
            "_removeLiquidityOneCoinAfter",
            "after <= before"
        );

        // Update post process
        if (tokenI != NATIVE_TOKEN_ADDRESS) _updateToken(tokenI);

        return balance - balanceBefore;
    }
}
