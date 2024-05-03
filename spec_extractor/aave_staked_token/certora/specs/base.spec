using DummyERC20Impl as stake_token
using DummyERC20Impl as reward_token

methods {

    stake_token.balanceOf(address) returns (uint256) envfree

    // public variables
    REWARDS_VAULT() returns (address) envfree
    UNSTAKE_WINDOW() returns (uint256) envfree
    LOWER_BOUND() returns (uint256) envfree
    INITIAL_EXCHANGE_RATE() returns (uint216) envfree

    // envfree
    balanceOf(address) returns (uint256) envfree
    cooldownAmount(address) returns (uint216) envfree
    cooldownTimestamp(address) returns (uint40) envfree
    totalSupply() returns (uint256) envfree
    stakerRewardsToClaim(address) returns (uint256) envfree
    stakersCooldowns(address) returns (uint40, uint216) envfree
    getCooldownSeconds() returns (uint256) envfree
    getExchangeRate() returns (uint216) envfree
    inPostSlashingPeriod() returns (bool) envfree
    getMaxSlashablePercentage() returns (uint256) envfree
    getAssetGlobalIndex(address) returns (uint256) envfree
    getUserPersonalIndex(address, address) returns (uint256) envfree
    previewStake(uint256) returns (uint256) envfree
    previewRedeem(uint256) returns (uint256) envfree
    permit(address, address, uint256, uint256, uint8, bytes32, bytes32) => NONDET

    // address, block, delegation type
    _votingSnapshotsCounts(address) returns (uint256) envfree
    _updateCurrentUnclaimedRewards(address, uint256, bool) returns (uint256) envfree

    // view but not envfree - uses block.timestamp
    getNextCooldownTimestamp(uint256,uint256,address,uint256)
    getPowerAtBlock(address,uint256,uint8) returns (uint256)

    // state changing operations
    initialize(address,address,address,uint256,uint256)
    stake(address,uint256)
    redeem(address,uint256)
    slash(address,uint256) returns (uint256)
    returnFunds(uint256)

    // variable debt token
    updateDiscountDistribution(address, address, uint256, uint256, uint256) => NONDET
}

definition AAVE_MAX_SUPPLY() returns uint256 = 16000000 * 10^18;
definition EXCHANGE_RATE_FACTOR() returns uint256 = 10^18;
definition PERCENTAGE_FACTOR() returns uint256 = 10^4;

// a reasonable assumption that slashing is below 99%
definition MAX_EXCHANGE_RATE() returns uint256 = 100 * 10^18;
definition MAX_PERCENTAGE() returns uint256 = 100 * PERCENTAGE_FACTOR();
definition INITIAL_EXCHANGE_RATE() returns uint256 = 10^18;
definition MAX_COOLDOWN() returns uint256 = 2302683158; //20 years from now

definition VOTING_POWER() returns uint8 = 0;
definition PROPOSITION_POWER() returns uint8 = 1;


definition claimRewards_funcs(method f) returns bool =
(
    f.selector == claimRewards(address, uint256).selector ||
    f.selector == claimRewardsOnBehalf(address, address, uint256).selector ||
    f.selector == claimRewardsAndStake(address, uint256).selector ||
    f.selector == claimRewardsAndStakeOnBehalf(address, address, uint256).selector ||
    f.selector == claimRewardsAndRedeem(address, uint256, uint256).selector ||
    f.selector == claimRewardsAndRedeemOnBehalf(address, address, uint256, uint256).selector
);

definition redeem_funcs(method f) returns bool =
(
    f.selector == redeem(address, uint256).selector ||
    f.selector == redeemOnBehalf(address, address, uint256).selector ||
    f.selector == claimRewardsAndRedeem(address, uint256, uint256).selector ||
    f.selector == claimRewardsAndRedeemOnBehalf(address, address, uint256, uint256).selector
);
