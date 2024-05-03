// SPDX-License-Identifier: AGPL-3.0
pragma solidity ^0.8.0;

interface IVariableDebtTokenV3 {

  // IVariableDebtTokenV3
  function mint(address user, address onBehalfOf, uint256 amount, uint256 index) external returns (bool, uint256);
  function burn(address from, uint256 amount, uint256 index) external returns (uint256);
  function UNDERLYING_ASSET_ADDRESS() external view returns (address);

  // IScaledBalanceToken
  function scaledBalanceOf(address user) external view returns (uint256);
  function getScaledUserBalanceAndSupply(address user) external view returns (uint256, uint256);
  function scaledTotalSupply() external view returns (uint256);

  // ICreditDelegationToken
  function approveDelegation(address delegatee, uint256 amount) external;
  function borrowAllowance(address fromUser, address toUser) external view returns (uint256);

  // ERC20
  function totalSupply() external view returns (uint256);
  function balanceOf(address account) external view returns (uint256);
  function transfer(address recipient, uint256 amount) external returns (bool);
  function allowance(address owner, address spender) external view returns (uint256);
  function approve(address spender, uint256 amount) external returns (bool);
}