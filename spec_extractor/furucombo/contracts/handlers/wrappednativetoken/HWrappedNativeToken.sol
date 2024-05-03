// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../HandlerBase.sol";
import "./IWrappedNativeToken.sol";

contract HWrappedNativeToken is HandlerBase {
    // prettier-ignore
    address public immutable wrappedNativeToken;

    constructor(address wrappedNativeToken_) {
        wrappedNativeToken = wrappedNativeToken_;
    }

    function getContractName() public pure override returns (string memory) {
        return "HWrappedNativeToken";
    }

    function deposit(uint256 value) external payable {
        try
            IWrappedNativeToken(wrappedNativeToken).deposit{value: value}()
        {} catch Error(string memory reason) {
            _revertMsg("deposit", reason);
        } catch {
            _revertMsg("deposit");
        }
        _updateToken(wrappedNativeToken);
    }

    function withdraw(uint256 wad) external payable {
        try
            IWrappedNativeToken(wrappedNativeToken).withdraw(wad)
        {} catch Error(string memory reason) {
            _revertMsg("withdraw", reason);
        } catch {
            _revertMsg("withdraw");
        }
    }
}
