// SPDX-License-Identifier: agpl-3.0
pragma solidity 0.8.10;

import {IAaveIncentivesController} from "../interfaces/IAaveIncentivesController.sol";
import {IERC20} from "@aave/core-v3/contracts/dependencies/openzeppelin/contracts/IERC20.sol";

contract IncentivesControllerMock is IAaveIncentivesController {
    address public override REWARD_TOKEN;

    function setRewardToken(address rewardToken) external {
        REWARD_TOKEN = rewardToken;
    }

    function getAssetData(address)
        external
        view
        override
        returns (
            uint256,
            uint256,
            uint256
        )
    {
        return (0, 0, 0);
    }

    function assets(address)
        external
        view
        override
        returns (
            uint128,
            uint128,
            uint256
        )
    {
        return (0, 0, 0);
    }

    function setClaimer(address, address) external override {}

    function getClaimer(address) external view override returns (address) {
        return address(1);
    }

    function configureAssets(address[] calldata, uint256[] calldata)
        external
        override
    {}

    function handleAction(
        address,
        uint256,
        uint256
    ) external override {}

    function getRewardsBalance(address[] calldata, address)
        external
        view
        override
        returns (uint256)
    {
        return 0;
    }

    function claimRewards(
        address[] calldata,
        uint256,
        address
    ) external override returns (uint256) {
        return 0;
    }

    function claimRewardsOnBehalf(
        address[] calldata,
        uint256,
        address,
        address
    ) external override returns (uint256) {
        return 0;
    }

    function getUserUnclaimedRewards(address)
        external
        view
        override
        returns (uint256)
    {
        return 0;
    }

    function getUserAssetData(address, address)
        external
        view
        override
        returns (uint256)
    {
        return 0;
    }

    function PRECISION() external view override returns (uint8) {
        return 0;
    }

    function DISTRIBUTION_END() external view override returns (uint256) {
        return 0;
    }

    function EMISSION_MANAGER() external view returns (address) {
        return address(0);
    }

    function setDistributionEnd(uint256 distributionEnd) external {}
}
