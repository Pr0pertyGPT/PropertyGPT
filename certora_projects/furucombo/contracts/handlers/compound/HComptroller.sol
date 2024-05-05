// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "../HandlerBase.sol";
import "./IComptroller.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract HComptroller is HandlerBase {
    using SafeERC20 for IERC20;

    // prettier-ignore
    address public constant COMPTROLLER = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;

    function getContractName() public pure override returns (string memory) {
        return "HComptroller";
    }

    function claimComp() external payable returns (uint256) {
        IComptroller comptroller = IComptroller(COMPTROLLER);
        address comp = comptroller.getCompAddress();
        address sender = _getSender();

        uint256 beforeCompBalance = IERC20(comp).balanceOf(sender);
        try comptroller.claimComp(sender) {} catch Error(string memory reason) {
            _revertMsg("claimComp", reason);
        } catch {
            _revertMsg("claimComp");
        }
        uint256 afterCompBalance = IERC20(comp).balanceOf(sender);

        return afterCompBalance - beforeCompBalance;
    }

    function claimComp(address holder) external payable returns (uint256) {
        IComptroller comptroller = IComptroller(COMPTROLLER);
        address comp = comptroller.getCompAddress();

        uint256 beforeCompBalance = IERC20(comp).balanceOf(holder);
        try comptroller.claimComp(holder) {} catch Error(string memory reason) {
            _revertMsg("claimComp", reason);
        } catch {
            _revertMsg("claimComp");
        }
        uint256 afterCompBalance = IERC20(comp).balanceOf(holder);

        return afterCompBalance - beforeCompBalance;
    }
}
