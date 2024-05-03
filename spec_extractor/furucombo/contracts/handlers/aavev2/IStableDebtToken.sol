// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IStableDebtToken{
  function getAverageStableRate() external view returns (uint256);
  function getUserLastUpdated(address user) external view returns (uint40);
  function getUserStableRate(address user) external view returns (uint256);
  function balanceOf(address account) external view returns (uint256);
  function mint( address user, address onBehalfOf, uint256 amount, uint256 rate) external returns (bool);
  function burn(address user, uint256 amount) external;
  function getSupplyData() external view returns (uint256, uint256, uint256, uint40);
  function getTotalSupplyAndAvgRate() external view returns (uint256, uint256);
  function totalSupply() external view returns (uint256);
  function getTotalSupplyLastUpdated() external view returns (uint40);
  function principalBalanceOf(address user) external view returns (uint256);

  function approveDelegation(address delegatee, uint256 amount) external;
  function borrowAllowance(address fromUser, address toUser) external view returns (uint256);
  function transfer(address recipient, uint256 amount) external returns (bool);
  function allowance(address owner, address spender) external view returns (uint256);
  function approve(address spender, uint256 amount) external returns (bool);
}
