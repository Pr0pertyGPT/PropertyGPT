// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IFunds{
    function denomination() external view returns (address);
    function shareToken() external view returns (address);
    function calculateShare(uint256 balance_) external view returns (uint256 share);
    function calculateBalance(uint256 share_) external view returns (uint256 balance);
    function vault() external view returns (address);

    function purchase(uint256 balance_) external returns (uint256 share);
    function redeem(uint256 share_, bool acceptPending_) external returns (uint256 balance);
}
