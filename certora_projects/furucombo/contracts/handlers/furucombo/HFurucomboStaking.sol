// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import "../HandlerBase.sol";
import "./IStaking.sol";
import "./IMerkleRedeem.sol";

contract HFurucomboStaking is HandlerBase {
    using SafeERC20 for IERC20;

    function getContractName() public pure override returns (string memory) {
        return "HFurucomboStaking";
    }

    function stake(address pool, uint256 amount) external payable {
        IStaking staking = IStaking(pool);
        address stakeToken = staking.stakingToken();
        amount = _getBalance(stakeToken, amount);
        require(amount > 0, "HFurucombo: stake amount = 0");

        _tokenApprove(stakeToken, pool, amount);
        staking.stakeFor(_getSender(), amount);
        _tokenApproveZero(stakeToken, pool);
    }

    function unstake(address pool, uint256 amount) external payable {
        require(amount > 0, "HFurucombo: unstake amount = 0");
        IStaking staking = IStaking(pool);
        staking.unstakeFor(_getSender(), amount);

        // Update involved token
        _updateToken(staking.stakingToken());
    }

    function claimAll(
        address user,
        address[] calldata pools,
        IMerkleRedeem.Claim[][] calldata claims
    ) external payable {
        require(claims.length > 0, "HFurucombo: claims length = 0");
        require(
            pools.length == claims.length,
            "HFurucombo: pools length != claims length"
        );

        for (uint256 i = 0; i < claims.length; i++) {
            IMerkleRedeem redeem = IMerkleRedeem(pools[i]);
            redeem.claimWeeks(user, claims[i]);
        }
    }
}
