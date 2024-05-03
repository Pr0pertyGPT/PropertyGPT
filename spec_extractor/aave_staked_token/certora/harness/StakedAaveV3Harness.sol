// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.0;

import {StakedAaveV3} from '../munged/contracts/StakedAaveV3.sol';
import {IERC20} from '../munged/interfaces/IERC20.sol';

contract StakedAaveV3Harness is StakedAaveV3 {
  constructor(
    IERC20 stakedToken,
    IERC20 rewardToken,
    uint256 unstakeWindow,
    address rewardsVault,
    address emissionManager,
    uint128 distributionDuration
  )
    StakedAaveV3(
      stakedToken,
      rewardToken,
      unstakeWindow,
      rewardsVault,
      emissionManager,
      distributionDuration
    )
  {}

  // Returns amount of the cooldown initiated by the user.
  function cooldownAmount(address user) public view returns (uint216) {
    return stakersCooldowns[user].amount;
  }

  // Returns timestamp of the cooldown initiated by the user.
  function cooldownTimestamp(address user) public view returns (uint40) {
    return stakersCooldowns[user].timestamp;
  }

  // Returns the asset's emission per second from the sturct
  function getAssetEmissionPerSecond(address token)
    public
    view
    returns (uint128)
  {
    return assets[token].emissionPerSecond;
  }

  // Returns the asset's last updated timestamp from the sturct
  function getAssetLastUpdateTimestamp(address token)
    public
    view
    returns (uint128)
  {
    return assets[token].lastUpdateTimestamp;
  }

  // Returns the asset's global index from the sturct
  function getAssetGlobalIndex(address token) public view returns (uint256) {
    return assets[token].index;
  }

  // Returns the user's personal index for the specific asset
  function getUserPersonalIndex(address token, address user)
    public
    view
    returns (uint256)
  {
    return assets[token].users[user];
  }

  function _getExchangeRateWrapper(uint256 totalAssets, uint256 totalShares)
    public
    pure
    returns (uint216)
  {
    return _getExchangeRate(totalAssets, totalShares);
  }
}
