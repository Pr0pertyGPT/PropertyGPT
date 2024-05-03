// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../HandlerBase.sol";
import "./ICToken.sol";

contract HCToken is HandlerBase {
    using SafeERC20 for IERC20;

    function getContractName() public pure override returns (string memory) {
        return "HCToken";
    }

    function mint(
        address cToken,
        uint256 mintAmount
    ) external payable returns (uint256) {
        // Get ctoken balance of proxy before mint
        ICToken compound = ICToken(cToken);
        uint256 beforeCTokenAmount = compound.balanceOf(address(this));

        address token = _getToken(cToken);
        // if amount == type(uint256).max return balance of Proxy
        mintAmount = _getBalance(token, mintAmount);
        _tokenApprove(token, cToken, mintAmount);
        try compound.mint(mintAmount) returns (uint256 errorCode) {
            _requireMsg(
                errorCode == 0,
                "mint",
                string(abi.encodePacked("error ", _uint2String(errorCode)))
            );
        } catch Error(string memory reason) {
            _revertMsg("mint", reason);
        } catch {
            _revertMsg("mint");
        }
        _tokenApproveZero(token, cToken);

        // Get ctoken balance of proxy after mint
        uint256 afterCTokenAmount = compound.balanceOf(address(this));

        // Update involved token
        _updateToken(cToken);
        return afterCTokenAmount - beforeCTokenAmount;
    }

    function redeem(
        address cToken,
        uint256 redeemTokens
    ) external payable returns (uint256) {
        // Get token balance of proxy before redeem
        address token = _getToken(cToken);
        uint256 beforeTokenAmount = IERC20(token).balanceOf(address(this));

        ICToken compound = ICToken(cToken);
        // if amount == type(uint256).max return balance of Proxy
        redeemTokens = _getBalance(cToken, redeemTokens);
        try compound.redeem(redeemTokens) returns (uint256 errorCode) {
            _requireMsg(
                errorCode == 0,
                "redeem",
                string(abi.encodePacked("error ", _uint2String(errorCode)))
            );
        } catch Error(string memory reason) {
            _revertMsg("redeem", reason);
        } catch {
            _revertMsg("redeem");
        }

        // Get token balance of proxy after redeem
        uint256 afterTokenAmount = IERC20(token).balanceOf(address(this));

        // Update involved token
        _updateToken(token);
        return afterTokenAmount - beforeTokenAmount;
    }

    function redeemUnderlying(
        address cToken,
        uint256 redeemAmount
    ) external payable returns (uint256) {
        // Get ctoken balance of proxy before redeem
        ICToken compound = ICToken(cToken);
        uint256 beforeCTokenAmount = compound.balanceOf(address(this));

        try compound.redeemUnderlying(redeemAmount) returns (
            uint256 errorCode
        ) {
            _requireMsg(
                errorCode == 0,
                "redeemUnderlying",
                string(abi.encodePacked("error ", _uint2String(errorCode)))
            );
        } catch Error(string memory reason) {
            _revertMsg("redeemUnderlying", reason);
        } catch {
            _revertMsg("redeemUnderlying");
        }

        // Get ctoken balance of proxy after redeem
        uint256 afterCTokenAmount = compound.balanceOf(address(this));

        // Update involved token
        address token = _getToken(cToken);
        _updateToken(token);
        return beforeCTokenAmount - afterCTokenAmount;
    }

    function repayBorrowBehalf(
        address cToken,
        address borrower,
        uint256 repayAmount
    ) external payable returns (uint256) {
        ICToken compound = ICToken(cToken);
        address token = _getToken(cToken);

        uint256 debt = compound.borrowBalanceCurrent(borrower);
        if (repayAmount < debt) {
            debt = repayAmount;
        }
        _tokenApprove(token, cToken, debt);
        try compound.repayBorrowBehalf(borrower, debt) returns (
            uint256 errorCode
        ) {
            _requireMsg(
                errorCode == 0,
                "repayBorrowBehalf",
                string(abi.encodePacked("error ", _uint2String(errorCode)))
            );
        } catch Error(string memory reason) {
            _revertMsg("repayBorrowBehalf", reason);
        } catch {
            _revertMsg("repayBorrowBehalf");
        }
        _tokenApproveZero(token, cToken);
        uint256 debtEnd = compound.borrowBalanceCurrent(borrower);
        return debtEnd;
    }

    function _getToken(address token) internal view returns (address result) {
        return ICToken(token).underlying();
    }
}
