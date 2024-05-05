// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IStableDebtTokenV3 {

  // IStableDebtToken
  function mint(address user, address onBehalfOf, uint256 amount, uint256 rate) external returns (bool, uint256, uint256);
  function burn(address from, uint256 amount) external returns (uint256, uint256);
  function getAverageStableRate() external view returns (uint256);
  function getUserStableRate(address user) external view returns (uint256);
  function getUserLastUpdated(address user) external view returns (uint40);
  function getSupplyData() external view returns (uint256, uint256, uint256, uint40);
  function getTotalSupplyLastUpdated() external view returns (uint40);
  function getTotalSupplyAndAvgRate() external view returns (uint256, uint256);
  function principalBalanceOf(address user) external view returns (uint256);
  function UNDERLYING_ASSET_ADDRESS() external view returns (address);

  // ICreditDelegationToken
  function approveDelegation(address delegatee, uint256 amount) external;
  function borrowAllowance(address fromUser, address toUser) external view returns (uint256);
  function delegationWithSig(address delegator, address delegatee, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s) external;

  // ERC20
  function totalSupply() external view returns (uint256);
  function balanceOf(address account) external view returns (uint256);
  function transfer(address recipient, uint256 amount) external returns (bool);
  function allowance(address owner, address spender) external view returns (uint256);
  function approve(address spender, uint256 amount) external returns (bool);
}
