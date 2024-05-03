// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../HandlerBase.sol";
import "./IYVault.sol";

contract HYVault is HandlerBase {
    using SafeERC20 for IERC20;

    function getContractName() public pure override returns (string memory) {
        return "HYVault";
    }

    function deposit(
        address vault,
        uint256 _amount
    ) external payable returns (uint256) {
        IYVault yVault = IYVault(vault);
        uint256 beforeYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );

        address token = yVault.token();
        // if amount == type(uint256).max return balance of Proxy
        _amount = _getBalance(token, _amount);
        _tokenApprove(token, address(yVault), _amount);
        try yVault.deposit(_amount) {} catch Error(string memory reason) {
            _revertMsg("deposit", reason);
        } catch {
            _revertMsg("deposit");
        }
        _tokenApproveZero(token, address(yVault));

        uint256 afterYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );

        _updateToken(address(yVault));
        return afterYTokenBalance - beforeYTokenBalance;
    }

    function depositETH(
        uint256 value,
        address vault
    ) external payable returns (uint256) {
        IYVault yVault = IYVault(vault);
        uint256 beforeYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );
        // if amount == type(uint256).max return balance of Proxy
        value = _getBalance(address(0), value);
        try yVault.depositETH{value: value}() {} catch Error(
            string memory reason
        ) {
            _revertMsg("depositETH", reason);
        } catch {
            _revertMsg("depositETH");
        }
        uint256 afterYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );

        _updateToken(address(yVault));
        return afterYTokenBalance - beforeYTokenBalance;
    }

    function withdraw(
        address vault,
        uint256 _shares
    ) external payable returns (uint256) {
        IYVault yVault = IYVault(vault);
        address token = yVault.token();
        uint256 beforeTokenBalance = IERC20(token).balanceOf(address(this));
        // if amount == type(uint256).max return balance of Proxy
        _shares = _getBalance(vault, _shares);

        try yVault.withdraw(_shares) {} catch Error(string memory reason) {
            _revertMsg("withdraw", reason);
        } catch {
            _revertMsg("withdraw");
        }
        uint256 afterTokenBalance = IERC20(token).balanceOf(address(this));

        _updateToken(token);
        return afterTokenBalance - beforeTokenBalance;
    }

    function withdrawETH(
        address vault,
        uint256 _shares
    ) external payable returns (uint256) {
        uint256 beforeETHBalance = address(this).balance;
        IYVault yVault = IYVault(vault);
        // if amount == type(uint256).max return balance of Proxy
        _shares = _getBalance(vault, _shares);
        try yVault.withdrawETH(_shares) {} catch Error(string memory reason) {
            _revertMsg("withdrawETH", reason);
        } catch {
            _revertMsg("withdrawETH");
        }
        uint256 afterETHBalance = address(this).balance;
        return afterETHBalance - beforeETHBalance;
    }
}
