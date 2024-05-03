// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IStakingRewardsAdapter {
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
    function isApproved(address owner, address agent) external view returns (bool);

    // Mutative
    function stake(uint256 amount) external;
    function withdraw(uint256 amount) external;
    function getReward() external;
    function exit() external;

    function stakeFor(address account, uint256 amount) external;
    function withdrawFor(address account, uint256 amount) external;
    function getRewardFor(address account) external;
    function exitFor(address account) external;

    function setApproval(address agent, bool approval) external;
}
