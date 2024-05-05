// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../HandlerBase.sol";
import "./ICEther.sol";

contract HCEther is HandlerBase {
    using SafeERC20 for IERC20;

    address public constant CETHER = 0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5;

    function getContractName() public pure override returns (string memory) {
        return "HCEther";
    }

    function mint(uint256 value) external payable returns (uint256) {
        ICEther compound = ICEther(CETHER);

        // Get cether balance of proxy before mint
        uint256 beforeCEtherAmount = compound.balanceOf(address(this));

        // if amount == type(uint256).max return balance of Proxy
        value = _getBalance(address(0), value);

        // Execute mint
        try compound.mint{value: value}() {} catch Error(string memory reason) {
            _revertMsg("mint", reason);
        } catch {
            _revertMsg("mint");
        }

        // Get cether balance of proxy after mint
        uint256 afterCEtherAmount = compound.balanceOf(address(this));

        // Update involved token
        _updateToken(CETHER);
        return (afterCEtherAmount - beforeCEtherAmount);
    }

    function redeem(uint256 redeemTokens) external payable returns (uint256) {
        // Get ether balance of proxy before redeem
        uint256 beforeRedeemAmount = address(this).balance;

        // Approve cether
        ICEther compound = ICEther(CETHER);

        // if amount == type(uint256).max return balance of Proxy
        redeemTokens = _getBalance(CETHER, redeemTokens);

        // Execute redeem
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

        // Get ether balance of proxy after redeem
        uint256 afterRedeemAmount = address(this).balance;
        return (afterRedeemAmount - beforeRedeemAmount);
    }

    function redeemUnderlying(
        uint256 redeemAmount
    ) external payable returns (uint256) {
        // Get cether balance of proxy before redeemUnderlying
        ICEther compound = ICEther(CETHER);
        uint256 beforeCEtherAmount = compound.balanceOf(address(this));

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

        // Get cether balance of proxy after redeemUnderlying
        uint256 afterCEtherAmount = compound.balanceOf(address(this));
        return (beforeCEtherAmount - afterCEtherAmount);
    }

    function repayBorrowBehalf(
        uint256 amount,
        address borrower
    ) external payable returns (uint256) {
        ICEther compound = ICEther(CETHER);
        uint256 debt = compound.borrowBalanceCurrent(borrower);

        if (amount < debt) {
            debt = amount;
        }
        try compound.repayBorrowBehalf{value: debt}(borrower) {} catch Error(
            string memory reason
        ) {
            _revertMsg("repayBorrowBehalf", reason);
        } catch {
            _revertMsg("repayBorrowBehalf");
        }
        uint256 debtEnd = compound.borrowBalanceCurrent(borrower);
        return debtEnd;
    }
}
