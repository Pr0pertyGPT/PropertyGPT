// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../HandlerBase.sol";
import "./IMinter.sol";
import "./ILiquidityGauge.sol";

contract HCurveDao is HandlerBase {
    using SafeERC20 for IERC20;

    // prettier-ignore
    address public constant CURVE_MINTER = 0xd061D61a4d941c39E5453435B6345Dc261C2fcE0;
    // prettier-ignore
    address public constant CRV_TOKEN = 0xD533a949740bb3306d119CC777fa900bA034cd52;

    function getContractName() public pure override returns (string memory) {
        return "HCurveDao";
    }

    function mint(address gaugeAddr) external payable returns (uint256) {
        IMinter minter = IMinter(CURVE_MINTER);
        address user = _getSender();
        uint256 beforeCRVBalance = IERC20(CRV_TOKEN).balanceOf(user);
        _requireMsg(
            minter.allowed_to_mint_for(address(this), user),
            "mint",
            "not allowed to mint"
        );

        try minter.mint_for(gaugeAddr, user) {} catch Error(
            string memory reason
        ) {
            _revertMsg("mint", reason);
        } catch {
            _revertMsg("mint");
        }
        uint256 afterCRVBalance = IERC20(CRV_TOKEN).balanceOf(user);

        _updateToken(CRV_TOKEN);
        return afterCRVBalance - beforeCRVBalance;
    }

    function mintMany(
        address[] calldata gaugeAddrs
    ) external payable returns (uint256) {
        IMinter minter = IMinter(CURVE_MINTER);
        address user = _getSender();
        uint256 beforeCRVBalance = IERC20(CRV_TOKEN).balanceOf(user);
        _requireMsg(
            minter.allowed_to_mint_for(address(this), user),
            "mintMany",
            "not allowed to mint"
        );

        for (uint256 i = 0; i < gaugeAddrs.length; i++) {
            try minter.mint_for(gaugeAddrs[i], user) {} catch Error(
                string memory reason
            ) {
                _revertMsg(
                    "mintMany",
                    string(abi.encodePacked(reason, " on ", _uint2String(i)))
                );
            } catch {
                _revertMsg(
                    "mintMany",
                    string(abi.encodePacked("Unspecified on ", _uint2String(i)))
                );
            }
        }

        _updateToken(CRV_TOKEN);
        return IERC20(CRV_TOKEN).balanceOf(user) - beforeCRVBalance;
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
