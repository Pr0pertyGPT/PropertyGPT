// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "../HandlerBase.sol";
import "./ILido.sol";

contract HLido is HandlerBase {
    address public immutable referral;
    ILido public immutable lidoProxy;

    constructor(address lidoProxy_, address referral_) {
        referral = referral_;
        lidoProxy = ILido(lidoProxy_);
    }

    function getContractName() public pure override returns (string memory) {
        return "HLido";
    }

    function submit(
        uint256 value
    ) external payable returns (uint256 stTokenAmount) {
        // if amount == type(uint256).max return balance of Proxy
        value = _getBalance(NATIVE_TOKEN_ADDRESS, value);

        try lidoProxy.submit{value: value}(referral) returns (
            uint256 sharesAmount
        ) {
            stTokenAmount = lidoProxy.getPooledEthByShares(sharesAmount);
        } catch Error(string memory reason) {
            _revertMsg("submit", reason);
        } catch {
            _revertMsg("submit");
        }

        _updateToken(address(lidoProxy));
    }
}
