// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "../HandlerBase.sol";
import "./IRootChainManager.sol";
import "./IDepositManager.sol";

contract HPolygon is HandlerBase {
    using SafeERC20 for IERC20;

    // prettier-ignore
    IDepositManager public constant PLASMA_MANAGER = IDepositManager(0x401F6c983eA34274ec46f84D70b31C151321188b);
    // prettier-ignore
    IRootChainManager public constant POS_MANAGER = IRootChainManager(0xA0c68C638235ee32657e8f720a23ceC1bFc77C77);
    // prettier-ignore
    address public constant POS_PREDICATE_ERC20 = 0x40ec5B33f54e0E8A33A975908C5BA1c14e5BbbDf;
    // prettier-ignore
    address public constant MATIC_ADDRESS = 0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0;

    event PolygonBridged(
        address indexed sender,
        address indexed token,
        uint256 amount
    );

    function getContractName() public pure override returns (string memory) {
        return "HPolygon";
    }

    function depositEther(uint256 value) external payable {
        address user = _getSender();
        value = _getBalance(address(0), value);

        // Use PoS bridge for ether
        try POS_MANAGER.depositEtherFor{value: value}(user) {} catch Error(
            string memory reason
        ) {
            _revertMsg("depositEther", reason);
        } catch {
            _revertMsg("depositEther");
        }

        emit PolygonBridged(user, NATIVE_TOKEN_ADDRESS, value);
    }

    function depositERC20(address token, uint256 amount) external payable {
        address user = _getSender();
        amount = _getBalance(token, amount);

        if (token == MATIC_ADDRESS) {
            // Use Plasma bridge for MATIC token
            _tokenApprove(token, address(PLASMA_MANAGER), amount);
            try
                PLASMA_MANAGER.depositERC20ForUser(token, user, amount)
            {} catch Error(string memory reason) {
                _revertMsg("depositERC20", reason);
            } catch {
                _revertMsg("depositERC20");
            }
            _tokenApproveZero(token, address(PLASMA_MANAGER));
        } else {
            // Use PoS bridge for other tokens
            bytes memory depositData = abi.encodePacked(amount);
            _tokenApprove(token, POS_PREDICATE_ERC20, amount);
            try POS_MANAGER.depositFor(user, token, depositData) {} catch Error(
                string memory reason
            ) {
                _revertMsg("depositERC20", reason);
            } catch {
                _revertMsg("depositERC20");
            }
            _tokenApproveZero(token, POS_PREDICATE_ERC20);
        }

        emit PolygonBridged(user, token, amount);
    }
}
