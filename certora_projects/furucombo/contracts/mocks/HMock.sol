// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../handlers/HandlerBase.sol";

interface IFaucet {
    function drain() external payable;

    function drainToken(address token, uint256 amount) external;
}

contract HMock is HandlerBase {
    using SafeERC20 for IERC20;

    function getContractName() public pure override returns (string memory) {
        return "HMock";
    }

    function drain(address target, uint256 v) external payable {
        IFaucet(target).drain{value: v}();
    }

    function drainToken(
        address target,
        address token,
        uint256 amount
    ) external payable {
        _tokenApprove(token, target, amount);
        IFaucet(target).drainToken(token, amount);
        _tokenApproveZero(token, target);
        _updateToken(token);
    }

    function drainTokens(
        address[] calldata targets,
        address[] calldata tokens,
        uint256[] calldata amounts
    ) external payable {
        for (uint256 i = 0; i < targets.length; i++) {
            _tokenApprove(tokens[i], targets[i], amounts[i]);
            IFaucet(targets[i]).drainToken(tokens[i], amounts[i]);
            _tokenApproveZero(tokens[i], targets[i]);
            _updateToken(tokens[i]);
        }
    }

    function updatePostProcess(bytes32[] memory params) external payable {
        _updatePostProcess(params);
    }

    function tokenApprove(
        address token,
        address spender,
        uint256 amount
    ) external payable {
        _tokenApprove(token, spender, amount);
    }
}
