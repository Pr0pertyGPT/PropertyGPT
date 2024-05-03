import "invariants.spec"
import "propertiesWithSummarizations.spec"

use invariant allSharesAreBacked
use invariant cooldownAmountNotGreaterThanBalance
use invariant cooldownDataCorrectness // this is imported because we use it in invariants.spec
use invariant lowerBoundNotZero
use invariant PersonalIndexLessOrEqualGlobalIndex
use invariant totalSupplyGreaterThanUserBalance // this is imported because we use it in invariants.spec

/*
    @Rule integrityOfStaking
    @Description: successful stake function move amount of the stake token from the sender to the contract
                  and increases the sender's shares balance accordinly.

    @Formula:
        {
            balanceStakeTokenDepositorBefore := stake_token.balanceOf(msg.sender),
            balanceStakeTokenVaultBefore := stake_token.balanceOf(currentContract),
            balanceBefore := balanceOf(onBehalfOf)
        }
            stake(onBehalfOf, amount)
        {
            balanceOf(onBehalfOf) = balanceBefore + amount * currentExchangeRate / EXCHANGE_RATE_FACTOR,
            stake_token.balanceOf(msg.sender) = balanceStakeTokenDepositorBefore - amount,
            stake_token.balanceOf(currentContract) = balanceStakeTokenVaultBefore + amount
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule integrityOfStaking(address onBehalfOf, uint256 amount) {
    env e;
    require(amount < AAVE_MAX_SUPPLY());
    require(e.msg.sender != currentContract);

    uint256 balanceStakeTokenDepositorBefore = stake_token.balanceOf(e.msg.sender);
    uint256 balanceStakeTokenVaultBefore = stake_token.balanceOf(currentContract);
    uint256 balanceBefore = balanceOf(onBehalfOf);
    require(balanceStakeTokenDepositorBefore < AAVE_MAX_SUPPLY());
    require(balanceStakeTokenVaultBefore < AAVE_MAX_SUPPLY());
    require(balanceBefore < AAVE_MAX_SUPPLY());
    uint72 cooldownBefore;
    cooldownBefore, _ = stakersCooldowns(onBehalfOf);
    require(cooldownBefore == 0);
    stake(e, onBehalfOf, amount);
    uint256 balanceAfter = balanceOf(onBehalfOf);
    uint72 cooldownAfter;
    cooldownAfter, _ = stakersCooldowns(onBehalfOf);
    uint256 balanceStakeTokenDepositorAfter = stake_token.balanceOf(e.msg.sender);
    uint256 balanceStakeTokenVaultAfter = stake_token.balanceOf(currentContract);

    uint216 currentExchangeRate = getExchangeRate();

    assert balanceAfter == balanceBefore +
        amount * currentExchangeRate / EXCHANGE_RATE_FACTOR();
    assert balanceStakeTokenDepositorAfter == balanceStakeTokenDepositorBefore - amount;
    assert balanceStakeTokenVaultAfter == balanceStakeTokenVaultBefore + amount;
}

/*
    @Rule noStakingPostSlashingPeriod
    @Description: Rule to verify that no user can stake while in post-slashing period.

    @Formula:
            stake(onBehalfOf, amount)
        {
            inPostSlashingPeriod = true => function reverts
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule noStakingPostSlashingPeriod(address onBehalfOf, uint256 amount) {
    env e;
    require(inPostSlashingPeriod());
    stake@withrevert(e, onBehalfOf, amount);
    assert lastReverted, "should not be able to stake in post slashing period";
}

/*
    @Rule noSlashingMoreThanMax
    @Description: Rule to verify that slashing can't exceed the available slashing amount.

    @Formula:
        {
            vaultBalanceBefore := stake_token.balanceOf(currentContract),
            maxSlashable := vaultBalanceBefore * MaxSlashablePercentage / PERCENTAGE_FACTOR
        }
            slash(recipient, amount)
        {
            vaultBalanceBefore - stake_token.balanceOf(currentContract) = maxSlashable
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule noSlashingMoreThanMax(uint256 amount, address recipient){
    env e;
    uint vaultBalanceBefore = stake_token.balanceOf(currentContract);
    require(vaultBalanceBefore < AAVE_MAX_SUPPLY());
    require(getMaxSlashablePercentage() >= PERCENTAGE_FACTOR() &&
        getMaxSlashablePercentage() <= MAX_PERCENTAGE());
    uint256 maxSlashable = vaultBalanceBefore * getMaxSlashablePercentage() / PERCENTAGE_FACTOR();

    require (amount > maxSlashable);
    require (recipient != currentContract);
    slash(e, recipient, amount);
    uint vaultBalanceAfter = stake_token.balanceOf(currentContract);

    assert vaultBalanceBefore - vaultBalanceAfter == maxSlashable;
}

/*
    @Rule integrityOfSlashing
    @Description: successful slash function increases the recipient balance by the slashed amount,
                  decreases the vaults balance by the same amount and turns on the postSlashing period flag.

    @Formula:
        {
            recipientStakeTokenBalanceBefore := stake_token.balanceOf(recipient),
            vaultStakeTokenBalanceBefore := stake_token.balanceOf(currentContract)
        }
            slash(recipient, amountToSlash)
        {
            stake_token.balanceOf(recipient) = recipientStakeTokenBalanceBefore + amountToSlash,
            stake_token.balanceOf(currentContract) = vaultStakeTokenBalanceBefore - amountToSlash,
            inPostSlashingPeriod = True
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule integrityOfSlashing(address to, uint256 amount){
    env e;
    require(amount < AAVE_MAX_SUPPLY());
    require(e.msg.sender != currentContract && to != currentContract);
    require(getMaxSlashablePercentage() >= PERCENTAGE_FACTOR() &&
        getMaxSlashablePercentage() <= MAX_PERCENTAGE());

    require(totalSupply() > 0 && totalSupply() < AAVE_MAX_SUPPLY());
    uint256 total = totalSupply();

    uint256 balanceStakeTokenToBefore = stake_token.balanceOf(to);
    uint256 balanceStakeTokenVaultBefore = stake_token.balanceOf(currentContract);
    require(balanceStakeTokenToBefore < AAVE_MAX_SUPPLY());
    require(balanceStakeTokenVaultBefore < AAVE_MAX_SUPPLY());
    slash(e, to, amount);
    uint256 balanceStakeTokenToAfter = stake_token.balanceOf(to);
    uint256 balanceStakeTokenVaultAfter = stake_token.balanceOf(currentContract);
    uint256 maxSlashable = balanceStakeTokenVaultBefore * getMaxSlashablePercentage() / PERCENTAGE_FACTOR();

    uint256 amountToSlash;
    if (amount > maxSlashable) {
        amountToSlash = maxSlashable;
    } else {
        amountToSlash = amount;
    }

    assert balanceStakeTokenToAfter == balanceStakeTokenToBefore + amountToSlash;
    assert balanceStakeTokenVaultAfter == balanceStakeTokenVaultBefore - amountToSlash;
    assert inPostSlashingPeriod();
}

/*
    @Rule integrityOfReturnFunds
    @Description: successful returnFunds function decreases the sender balance by the returned amount and
                  increases the vaults balance by the same amount.

    @Formula:
        {
            senderStakeTokenBalanceBefore := stake_token.balanceOf(msg.sender),
            vaultStakeTokenBalanceBefore := stake_token.balanceOf(currentContract)
        }
            returnFunds(amount)
        {
            stake_token.balanceOf(msg.sender) = recipientStakeTokenBalanceBefore - amount,
            stake_token.balanceOf(currentContract) = vaultStakeTokenBalanceBefore + amount
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule integrityOfReturnFunds(uint256 amount){
    env e;
    require(amount < AAVE_MAX_SUPPLY());
    require(e.msg.sender != currentContract);

    uint256 balanceStakeTokenSenderBefore = stake_token.balanceOf(e.msg.sender);
    uint256 balanceStakeTokenVaultBefore = stake_token.balanceOf(currentContract);
    require(balanceStakeTokenSenderBefore < AAVE_MAX_SUPPLY());
    require(balanceStakeTokenVaultBefore < AAVE_MAX_SUPPLY());
    returnFunds(e, amount);
    uint256 balanceStakeTokenSenderAfter = stake_token.balanceOf(e.msg.sender);
    uint256 balanceStakeTokenVaultAfter = stake_token.balanceOf(currentContract);
    require(balanceStakeTokenVaultAfter > 0);

    assert balanceStakeTokenSenderAfter == balanceStakeTokenSenderBefore - amount;
    assert balanceStakeTokenVaultAfter == balanceStakeTokenVaultBefore + amount;
}

/*
    @Rule noEntryUntilSlashingSettled
    @Description: Rule to verify that users can't stake while until slashing is settled (after post-slashing period).

    @Formula:
        {
        }
            stake@withrevert(msg.sender, amount)
        {
            inPostSlashingPeriod => stake function reverted.
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule noEntryUntilSlashingSettled(uint256 amount){
    env e;

    stake@withrevert(e, e.msg.sender, amount);

    bool reverted = lastReverted;
    assert inPostSlashingPeriod() => reverted;
}

/*
    @Rule airdropNotMutualized
    @Description: Rule to verify that transfering tokens to the contract doesn't change the exchange rate.

    @Formula:
        {
            exchangeRateBefore := getExchangeRate()
        }
            stake_token.transfer(currentContract, amount)
        {
            getExchangeRate() => exchangeRateBefore
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule airdropNotMutualized(uint256 amount){
    env e;
    uint216 exchangeRateBefore = getExchangeRate();
    stake_token.transfer(e, currentContract, amount);
    uint216 exchangeRateAfter = getExchangeRate();
    assert exchangeRateBefore == exchangeRateAfter;
}

/*
    @Rule noRedeemOutOfUnstakeWindow
    @Description: Succesful redeem function means that the user's timestamp in within the unstake window or it's a post slashing period.

    @Formula:
        {
            cooldown := stakersCooldowns(msg.sender)
        }
            redeem(to, amount)
        {
            (inPostSlashingPeriod = true) ||
            (block.timestamp > cooldown + getCooldownSeconds() &&
            block.timestamp - (cooldown + getCooldownSeconds()) <= UNSTAKE_WINDOW)
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule noRedeemOutOfUnstakeWindow(address to, uint256 amount){
    env e;

    uint72 cooldown;
    cooldown, _ = stakersCooldowns(e.msg.sender);
    redeem(e, to, amount);

    // assert cooldown is inside the unstake window or it's a post slashing period
    assert inPostSlashingPeriod() ||
     (e.block.timestamp > cooldown + getCooldownSeconds() &&
        e.block.timestamp - (cooldown + getCooldownSeconds()) <= UNSTAKE_WINDOW());
}

/*
    @Rule totalSupplyDoesNotDropToZero
    @Description: When the totalSupply is positive, it can never become zero.
    @Notes:
    @Link: https://prover.certora.com/output/40577/ff250297b015412ca205db4ed18253e3/?anonymousKey=09c506cb5a75a7ca18379f9650b482ac15cc1f67
*/
rule totalSupplyDoesNotDropToZero(method f, calldataarg args, env e)
filtered {
    f -> !f.isView && !redeem_funcs(f)
} {
    require totalSupply() > 0;

    f(e, args);

    assert totalSupply() > 0;
}

/*
    @Rule cooldownCorrectness
    @Description: Rule to verify the correctness of stakersCooldowns.

    @Notes: During unstake period, each user should be able to unstake at most
            the amount they had when the cooldown has been initiated.
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule cooldownCorrectness(env e)
{
    calldataarg args;
    address user = e.msg.sender;
    require(user != 0 && user != currentContract);
    requireInvariant cooldownAmountNotGreaterThanBalance(user);

    uint40 cooldownStart;
    uint216 sharesCooldownStart;
    uint256 amountToUnstake;
    address to;
    cooldownStart, sharesCooldownStart = stakersCooldowns(user); // timestamp when was the cooldown initiated
    uint256 sharesBefore = balanceOf(user); // number of shares


    require(sharesBefore >= sharesCooldownStart);
    // The following 3 requirements make sure we are in the unstake period
    require(cooldownStart > 0);
    require(e.block.timestamp > cooldownStart + getCooldownSeconds());
    require(e.block.timestamp - (cooldownStart + getCooldownSeconds()) <= UNSTAKE_WINDOW());

    redeem(e, to, amountToUnstake);
    uint256 soldShares = sharesBefore - balanceOf(user);

    assert amountToUnstake <= sharesCooldownStart => soldShares == amountToUnstake;
    assert amountToUnstake > sharesCooldownStart => soldShares == sharesCooldownStart;
}

/*
    @Rule rewardsGetterEquivalentClaim
    @Description: Rewards getter returns the same amount of max rewards the user deserve (if the user was to withdraw max).

    @Formula:
        {
            deservedRewards := getTotalRewardsBalance(from),
            receiverBalanceBefore := reward_token.balanceOf(receiver)
        }
            claimedAmount := claimRewardsOnBehalf(from, receiver, max_uint256)
        {
            deservedRewards = claimedAmount,
            reward_token.balanceOf(receiver) = receiverBalanceBefore + claimedAmount
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule rewardsGetterEquivalentClaim(method f, env e, address to, address from) {
    require to != REWARDS_VAULT();
    uint256 deservedRewards = getTotalRewardsBalance(e, from);
    uint256 _receiverBalance = reward_token.balanceOf(to);

    uint256 claimedAmount = claimRewardsOnBehalf(e, from, to, max_uint256);

    uint256 receiverBalance_ = reward_token.balanceOf(to);

    assert(deservedRewards == claimedAmount);
    assert(receiverBalance_ == _receiverBalance + claimedAmount);
}

/*
    @Rule rewardsMonotonicallyIncrease
    @Description: Rewards monotonically increasing as time progresses.

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule rewardsMonotonicallyIncrease(address user, env e, env e2) {
    uint256 _deservedRewards = getTotalRewardsBalance(e, user);

    require e2.block.timestamp >= e.block.timestamp;

    uint256 deservedRewards_ = getTotalRewardsBalance(e2, user);

    assert(deservedRewards_ >= _deservedRewards);
}

/*
    @Rule rewardsIncreaseForNonClaimFunctions
    @Description: Rewards monotonically increasing for non claim functions.

    @Formula:
        {
            deservedRewardsBefore := getTotalRewardsBalance(user)
        }
            <invoke any method f>
        {
            deservedRewardsAfter := getTotalRewardsBalance(user)

            f != claimRewards(address, uint256) &&
            f != claimRewardsOnBehalf(address, address, uint256) &&
            f != claimRewardsAndStake(address, uint256) &&
            f != claimRewardsAndStakeOnBehalf(address, address, uint256) &&
            f != claimRewardsAndRedeem(address, uint256, uint256) &&
            f != claimRewardsAndRedeemOnBehalf(address, address, uint256, uint256)
            => deservedRewardsBefore <= deservedRewardsAfter
        }
    @Notes: We skip verification for view functions as those cannot change anything.
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule rewardsIncreaseForNonClaimFunctions(method f, address user, env e)
filtered {
    f -> !f.isView && !claimRewards_funcs(f)
} {
    uint256 _deservedRewards = getTotalRewardsBalance(e, user);

    requireInvariant totalSupplyGreaterThanUserBalance(user);
    requireInvariant allSharesAreBacked();

    calldataarg args;
    f(e, args);

    uint256 deservedRewards_ = getTotalRewardsBalance(e, user);

    assert(deservedRewards_ >= _deservedRewards);
}

/*
    @Rule indexesMonotonicallyIncrease
    @Description: Global index monotonically increasing.

    @Formula:
        {
            globalIndexBefore := getAssetGlobalIndex(asset),
            personalIndexBefore := getUserPersonalIndex(asset, user)
        }
            <invoke any method f>
        {
            getAssetGlobalIndex(asset) >= globalIndexBefore,
            getUserPersonalIndex(asset, user) >= personalIndexBefore
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule indexesMonotonicallyIncrease(method f, address asset, address user) {
    requireInvariant PersonalIndexLessOrEqualGlobalIndex(asset, user);
    uint256 _globalIndex = getAssetGlobalIndex(asset);
    uint256 _personalIndex = getUserPersonalIndex(asset, user);

    env e; calldataarg args;
    f(e, args);

    uint256 globalIndex_ = getAssetGlobalIndex(asset);
    uint256 personalIndex_ = getUserPersonalIndex(asset, user);

    assert(globalIndex_ >= _globalIndex);
    assert(personalIndex_ >= _personalIndex);
}

/*
    @Rule slashingIncreaseExchangeRate
    @Description: Slashing increases the exchange rate.

    @Formula:
        {
            ExchangeRateBefore := getExchangeRate()
        }
            slash(args)
        {
            getExchangeRate() >= ExchangeRateBefore
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule slashingIncreaseExchangeRate(address receiver, uint256 amount) {
    env e; calldataarg args;

    uint216 _ExchangeRate = getExchangeRate();

    slash(e, args);

    uint216 ExchangeRate_ = getExchangeRate();

    assert ExchangeRate_ >= _ExchangeRate;
}

/*
    @Rule returnFundsDecreaseExchangeRate
    @Description: Returning funds decreases the exchange rate.

    @Formula:
        {
            ExchangeRateBefore := getExchangeRate()
        }
            returnFunds(args)
        {
            getExchangeRate() <= ExchangeRateBefore
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule returnFundsDecreaseExchangeRate(address receiver, uint256 amount) {
    env e;
    uint216 _ExchangeRate = getExchangeRate();

    // Currently, in the constructor, LOWER_BOUND = 10**decimals
    requireInvariant lowerBoundNotZero();

    returnFunds(e, amount);

    uint216 ExchangeRate_ = getExchangeRate();

    assert ExchangeRate_ <= _ExchangeRate;
}

/*
    @Rule exchangeRateNeverZero
    @Description: ExchangeRate can never be zero.

    @Formula:
        {
            ExchangeRateBefore := getExchangeRate()
        }
            <invoke any method f>
        {
            getExchangeRate() != 0
        }

    @Notes: We used the following require to prove, that violation of this rule happened
            when totalSupply() == 0:
            require f.selector == returnFunds(uint256).selector => totalSupply() != 0;
            This has been solved by Lukas in this commit:
            https://github.com/Certora/aave-stk-slashing-mgmt/pull/1/commits/8336dc0747965a06c7dc39b4f89273c4ef7ed18a
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule exchangeRateNeverZero(method f) {
    env e; calldataarg args;
    uint216 _ER = getExchangeRate();
    require _ER != 0;

    f(e, args);

    uint216 ER_ = getExchangeRate();

    assert ER_ != 0;
}

/*
    @Rule slashAndReturnFundsOfZeroDoesntChangeExchangeRate
    @Description: Slashing 0 and returningFunds of 0 do not affect the exchange rate.

    @Formula:
        {
            ExchangeRateBefore := getExchangeRate()
        }
            slash(dest, 0) || returnFunds(0)
        {
            getExchangeRate() == ExchangeRateBefore
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule slashAndReturnFundsOfZeroDoesntChangeExchangeRate() {
    env e;
    address dest; uint256 amt = 0;
    uint216 _ER = getExchangeRate();
    storage initialStorage = lastStorage;

    slash(e, dest, amt);
    uint216 ER_AfterSlash = getExchangeRate();

    returnFunds(e, amt) at initialStorage;
    uint216 ER_AfterReturnFunds = getExchangeRate();

    assert(ER_AfterSlash == ER_AfterReturnFunds);
    assert(ER_AfterReturnFunds == _ER);
}

/*
    @Rule integrityOfRedeem
    @Description: When amount to redeem is not greater than the cooldown amount of the
        message sender, previewRedeem computes the same underlying amount as redeem.

    @Formula:
        {
            totalUnderlying := previewRedeem(amount),
            receiverBalanceBefore := stake_token.balanceOf(receiver)
        }
            redeem(receiver, amount)
        {
            receiverBalanceAfter := stake_token.balanceOf(receiver)
            amount <= cooldownAmount(e.msg.sender) =>
                totalUnderlying == receiverBalanceAfter - receiverBalanceBefore
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule integrityOfRedeem(method f, env e, address to, uint256 amount) {
    require balanceOf(e.msg.sender) >= amount;
    require currentContract != to;
    uint256 totalUnderlying = previewRedeem(amount);
    uint256 _receiverBalance = stake_token.balanceOf(to);

    redeem(e, to, amount);

    uint256 receiverBalance_ = stake_token.balanceOf(to);

    assert(amount <= cooldownAmount(e.msg.sender) =>
        totalUnderlying == receiverBalance_ - _receiverBalance);
}

/*
    @Rule previewStakeEquivalentStake
    @Description: Preview stake function returns the same shares amount to stake (doing the same calculation).

    @Formula:
        {
            amountOfShares := previewStake(amount),
            receiverBalanceBefore := balanceOf(receiver)
        }
            stake(receiver, amount)
        {
            amountOfShares = previewStake(amount) - receiverBalanceBefore
        }

    @Notes:
    @Link: https://prover.certora.com/output/40577/3fdb151c46c84b1ab323b99c80890273/?anonymousKey=68e37ada870b7b91c68a5eadaf6030f3989002a6
*/
rule previewStakeEquivalentStake(method f, env e, address to, uint256 amount){
    requireInvariant totalSupplyGreaterThanUserBalance(to);
    uint256 amountOfShares = previewStake(amount);
    uint256 _receiverBalance = balanceOf(to);

    stake(e, to, amount);

    uint256 receiverBalance_ = balanceOf(to);

    assert(amountOfShares == receiverBalance_ - _receiverBalance);
}
