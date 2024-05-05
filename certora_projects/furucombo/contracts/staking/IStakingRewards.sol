// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IStakingRewards {
    // Views
    function lastTimeRewardApplicable() external view returns (uint256);
    function rewardPerToken() external view returns (uint256);
    function earned(address account) external view returns (uint256);
    function getRewardForDuration() external view returns (uint256);
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function rewardsToken() external view returns (IERC20);
    function stakingToken() external view returns (IERC20);
    function rewardRate() external view returns (uint256);

    // Mutative
    function stake(uint256 amount) external;
    function withdraw(uint256 amount) external;
    function getReward() external;
    function exit() external;

    // Restricted
    function notifyRewardAmount(uint256 reward) external;
}
