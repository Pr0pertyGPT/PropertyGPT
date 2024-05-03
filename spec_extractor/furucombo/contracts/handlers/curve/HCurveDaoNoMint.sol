// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import {HandlerBase} from "../HandlerBase.sol";
import {ILiquidityGauge} from "./ILiquidityGauge.sol";

contract HCurveDaoNoMint is HandlerBase {
    function getContractName() public pure override returns (string memory) {
        return "HCurveDaoNoMint";
    }

    function deposit(address gaugeAddress, uint256 _value) external payable {
        ILiquidityGauge gauge = ILiquidityGauge(gaugeAddress);
        address token = gauge.lp_token();
        address user = _getSender();

        // if amount == type(uint256).max return balance of Proxy
        _value = _getBalance(token, _value);
        _tokenApprove(token, gaugeAddress, _value);

        try gauge.deposit(_value, user) {} catch Error(string memory reason) {
            _revertMsg("deposit", reason);
        } catch {
            _revertMsg("deposit");
        }
        _tokenApproveZero(token, gaugeAddress);
    }

    function withdraw(
        address gaugeAddress,
        uint256 _value
    ) external payable returns (uint256) {
        ILiquidityGauge gauge = ILiquidityGauge(gaugeAddress);
        address token = gauge.lp_token();

        _value = _getBalance(gaugeAddress, _value);

        try gauge.withdraw(_value) {} catch Error(string memory reason) {
            _revertMsg("withdraw", reason);
        } catch {
            _revertMsg("withdraw");
        }

        _updateToken(token);

        return _value;
    }
}
