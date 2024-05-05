// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "../../HandlerBase.sol";
import "./IFunds.sol";
import "./IFundProxyFactory.sol";

/// @title Furucombo funds operation handler.
/// @notice Deposit or withdraw to/from funds.
contract HFurucomboFunds is HandlerBase {
    using SafeERC20 for IERC20;
    using Strings for uint256;

    IFundProxyFactory public constant FUND_PROXY_FACTORY =
        IFundProxyFactory(0xFD1353baBf86387FcB6D009C7b74c1aB2178B304);

    function getContractName() public pure override returns (string memory) {
        return "HFurucomboFunds";
    }

    function purchase(
        address fundsAddr,
        uint256 amount
    ) external payable returns (uint256) {
        require(FUND_PROXY_FACTORY.isFundCreated(fundsAddr), "invalid funds");

        IFunds funds = IFunds(fundsAddr);
        address denomination = funds.denomination();
        amount = _getBalance(denomination, amount);

        // Purchase
        _tokenApprove(denomination, fundsAddr, amount);

        uint256 shareAmount;
        try funds.purchase(amount) returns (uint256 share_) {
            shareAmount = share_;
        } catch Error(string memory reason) {
            _revertMsg("purchase", reason);
        } catch (bytes memory data) {
            // The last 32 bytes should be Funds RevertCode.
            // Ex: 0x64c41b44000000000000000000000000000000000000000000000000000000000000004a
            uint256 revertCode;
            assembly {
                revertCode := mload(add(data, add(0x20, 4)))
            }
            _revertMsg("purchase", revertCode.toString());
        }

        _tokenApproveZero(denomination, fundsAddr);

        address shareToken = funds.shareToken();
        _updateToken(shareToken);

        return shareAmount;
    }

    function redeem(
        address fundsAddr,
        uint256 share
    ) external payable returns (uint256) {
        require(FUND_PROXY_FACTORY.isFundCreated(fundsAddr), "invalid funds");

        IFunds funds = IFunds(fundsAddr);
        address shareToken = funds.shareToken();
        share = _getBalance(shareToken, share);

        // Redeem, doesn't support redeem pending.
        _tokenApprove(shareToken, fundsAddr, share);

        uint256 amount;
        try funds.redeem(share, false) returns (uint256 balance) {
            amount = balance;
        } catch Error(string memory reason) {
            _revertMsg("redeem", reason);
        } catch (bytes memory data) {
            // The last 32 bytes should be Funds RevertCode.
            // Ex: 0x64c41b44000000000000000000000000000000000000000000000000000000000000004a
            uint256 revertCode;
            assembly {
                revertCode := mload(add(data, add(0x20, 4)))
            }
            _revertMsg("redeem", revertCode.toString());
        }

        _tokenApproveZero(shareToken, fundsAddr);

        address denomination = funds.denomination();
        _updateToken(denomination);

        return amount;
    }
}
