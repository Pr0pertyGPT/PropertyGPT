// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import "../HandlerBase.sol";
import "../maker/IDSProxy.sol";
import "./ICToken.sol";
import "./IComptroller.sol";

contract HSCompound is HandlerBase {
    using SafeERC20 for IERC20;

    // prettier-ignore
    address public constant FCOMPOUND_ACTIONS = 0x05EF8eb657027927fAB9b279138f0189CB144976;
    // prettier-ignore
    address public constant COMPTROLLER = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;
    // prettier-ignore
    address public constant CETH_ADDRESS = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;
    // prettier-ignore
    address public constant COMP_ADDRESS = 0xc00e94Cb662C3520282E6f5717214004A7f26888;

    function getContractName() public pure override returns (string memory) {
        return "HSCompound";
    }

    modifier isDSProxyOwner(address dsProxy) {
        address sender = _getSender();
        _requireMsg(
            IDSProxy(dsProxy).owner() == sender,
            "General",
            "Not owner of the DSProxy"
        );
        _;
    }

    function deposit(
        address dsProxy,
        address token,
        uint256 amount
    ) external payable isDSProxyOwner(dsProxy) {
        _deposit(dsProxy, token, amount);
    }

    function withdraw(
        address dsProxy,
        address token,
        uint256 amount
    ) external payable isDSProxyOwner(dsProxy) {
        _withdraw(dsProxy, token, amount);
        if (token != NATIVE_TOKEN_ADDRESS) _updateToken(token);
    }

    function borrow(
        address dsProxy,
        address cTokenIn,
        address cTokenBorrow,
        uint256 cAmountIn,
        uint256 uBorrowAmount,
        bool needEnterMarket
    ) external payable isDSProxyOwner(dsProxy) {
        if (cAmountIn > 0) {
            _deposit(dsProxy, cTokenIn, cAmountIn);
        }

        if (needEnterMarket) {
            _enterMarket(dsProxy, cTokenIn);
        }

        if (uBorrowAmount > 0) {
            address underlying;
            if (cTokenBorrow == CETH_ADDRESS) {
                underlying = NATIVE_TOKEN_ADDRESS;
            } else {
                underlying = _getToken(cTokenBorrow);
            }
            // Execute borrow, borrowed token will stay in the DSProxy
            try
                IDSProxy(dsProxy).execute(
                    FCOMPOUND_ACTIONS,
                    abi.encodeWithSelector(
                        // selector of "borrow(address,uint256)"
                        0x4b8a3529,
                        cTokenBorrow,
                        uBorrowAmount
                    )
                )
            {} catch Error(string memory reason) {
                _revertMsg("borrow", reason);
            } catch {
                _revertMsg("borrow");
            }
            // Withdraw borrowed token from the DSProxy
            _withdraw(dsProxy, underlying, uBorrowAmount);

            // Update borrowed token
            if (underlying != NATIVE_TOKEN_ADDRESS) _updateToken(underlying);
        }
    }

    function repayBorrow(
        address dsProxy,
        address cTokenRepay,
        address cTokenWithdraw,
        uint256 uRepayAmount,
        uint256 cWithdrawAmount
    ) external payable isDSProxyOwner(dsProxy) {
        // Execute repay only when `uRepayAmount` is greater than 0
        if (uRepayAmount > 0) {
            if (cTokenRepay == CETH_ADDRESS) {
                // Execute ether repay
                try
                    IDSProxy(dsProxy).execute{value: uRepayAmount}(
                        FCOMPOUND_ACTIONS,
                        abi.encodeWithSelector(
                            // selector of "repayBorrow(address,uint256)"
                            0xabdb5ea8,
                            cTokenRepay,
                            uRepayAmount
                        )
                    )
                {} catch Error(string memory reason) {
                    _revertMsg("repayBorrow", reason);
                } catch {
                    _revertMsg("repayBorrow");
                }
            } else {
                // Approve repay token to DSProxy
                address underlying = _getToken(cTokenRepay);
                _tokenApprove(underlying, dsProxy, uRepayAmount);
                // Execute token repay
                try
                    IDSProxy(dsProxy).execute(
                        FCOMPOUND_ACTIONS,
                        abi.encodeWithSelector(
                            // selector of "repayBorrow(address,uint256)"
                            0xabdb5ea8,
                            cTokenRepay,
                            uRepayAmount
                        )
                    )
                {} catch Error(string memory reason) {
                    _revertMsg("repayBorrow", reason);
                } catch {
                    _revertMsg("repayBorrow");
                }
                _tokenApproveZero(underlying, dsProxy);
            }
        }

        if (cWithdrawAmount > 0) {
            // Withdraw collateral from DSProxy
            _withdraw(dsProxy, cTokenWithdraw, cWithdrawAmount);
            // Update collateral token
            _updateToken(cTokenWithdraw);
        }
    }

    function enterMarket(
        address dsProxy,
        address cToken
    ) external payable isDSProxyOwner(dsProxy) {
        _enterMarket(dsProxy, cToken);
    }

    function enterMarkets(
        address dsProxy,
        address[] calldata cTokens
    ) external payable isDSProxyOwner(dsProxy) {
        try
            IDSProxy(dsProxy).execute(
                FCOMPOUND_ACTIONS,
                abi.encodeWithSelector(
                    // selector of "enterMarkets(address[])"
                    0xc2998238,
                    cTokens
                )
            )
        {} catch Error(string memory reason) {
            _revertMsg("enterMarkets", reason);
        } catch {
            _revertMsg("enterMarkets");
        }
    }

    function exitMarket(
        address dsProxy,
        address cToken
    ) external payable isDSProxyOwner(dsProxy) {
        try
            IDSProxy(dsProxy).execute(
                FCOMPOUND_ACTIONS,
                abi.encodeWithSelector(
                    // selector of "exitMarket(address)"
                    0xede4edd0,
                    cToken
                )
            )
        {} catch Error(string memory reason) {
            _revertMsg("exitMarket", reason);
        } catch {
            _revertMsg("exitMarket");
        }
    }

    function claimComp(
        address dsProxy
    ) external payable isDSProxyOwner(dsProxy) returns (uint256) {
        try IComptroller(COMPTROLLER).claimComp(dsProxy) {} catch Error(
            string memory reason
        ) {
            _revertMsg("claimComp", reason);
        } catch {
            _revertMsg("claimComp");
        }
        uint256 balance = IERC20(COMP_ADDRESS).balanceOf(dsProxy);
        // Withdraw whole COMP balance of DSProxy
        _withdraw(dsProxy, COMP_ADDRESS, balance);
        _updateToken(COMP_ADDRESS);

        return balance;
    }

    /* ========== INTERNAL FUNCTIONS ========== */

    function _deposit(address dsProxy, address token, uint256 amount) internal {
        if (token == NATIVE_TOKEN_ADDRESS) {
            address payable dsProxyPayable = payable(dsProxy);
            dsProxyPayable.transfer(amount);
        } else {
            IERC20(token).safeTransfer(dsProxy, amount);
        }
    }

    function _withdraw(
        address dsProxy,
        address token,
        uint256 amount
    ) internal {
        try
            IDSProxy(dsProxy).execute(
                FCOMPOUND_ACTIONS,
                abi.encodeWithSelector(
                    // selector of "withdraw(address,uint256)"
                    0xf3fef3a3,
                    token,
                    amount
                )
            )
        {} catch Error(string memory reason) {
            _revertMsg("_withdraw", reason);
        } catch {
            _revertMsg("_withdraw");
        }
    }

    function _enterMarket(address dsProxy, address cToken) internal {
        try
            IDSProxy(dsProxy).execute(
                FCOMPOUND_ACTIONS,
                abi.encodeWithSelector(
                    // selector of "enterMarket(address)"
                    0x3fe5d425,
                    cToken
                )
            )
        {} catch Error(string memory reason) {
            _revertMsg("_enterMarket", reason);
        } catch {
            _revertMsg("_enterMarket");
        }
    }

    function _getToken(address token) internal view returns (address) {
        return ICToken(token).underlying();
    }
}
