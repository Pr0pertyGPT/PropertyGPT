import "./LEValidStates.spec"

use invariant alwaysInitialized
use invariant oneStateOnly
use invariant factoryGetPairCorrelationCurrentVals
use invariant al_issuerAllocationZero
use invariant al_balanceLessThanAllocation
use invariant al_userAllocationLessThanMaxAllocation
use invariant al_issuerTimelockNonZero
use invariant al_userTimelockSeven
use invariant al_timelocksCorrelation
use invariant op_incentivesCorrelation
use invariant op_userNotWithdrawnPair
use invariant op_userNotWithdrawnIncentives
use invariant op_wavaxBalanceAndSumBalances
use invariant op_avaxAllocZero
use invariant op_lpSupplyZero
use invariant op_PairBalanceIsZero
use invariant op_AvaxCorrelation
use invariant op_PairAndTotalSupplyCorrelation
use invariant op_tokenCorrelation
use invariant cl_avaxAllocSumUserBalances
use invariant cl_avaxReservCheck
use invariant cl_incentivesCorrelation
use invariant cl_pairAndGetPairCorrelation
use invariant cl_AvaxCorrelation
use invariant os_tokenCorrelation
use invariant os_avaxAllocSumUserBalances



// STATUS - verified
// - token balance of this == tokenReserve + tokenIncentivesBalance
invariant hl_EqualityOfToken(env e) 
    getTokenBalanceOfThis() == tokenReserve() + tokenIncentivesBalance()
    {
        preserved with (env e2){
            safeAssumptions(e2);
            require e.msg.sender == e2.msg.sender;              
        }
    }


// STATUS - verified
// - additivity of deposit: deposit(a); deposit(b) has same effect as deposit(a+b)
rule hl_depositAdditivity(env e, env e2){
    require e.msg.value > 0;
    require e.msg.value == 2 * e2.msg.value;
    require e.msg.sender != e2.msg.sender;

    uint256 userOneBalanceBefore = getUserBalance(e.msg.sender);
    depositAVAX(e);
    uint256 userOneBalanceAfter = getUserBalance(e.msg.sender);
    
    uint256 userTwoBalanceBefore = getUserBalance(e2.msg.sender);
    require userOneBalanceBefore == userTwoBalanceBefore;
    depositAVAX(e2);
    depositAVAX(e2);
    uint256 userTwoBalanceAfter = getUserBalance(e2.msg.sender);

    assert userOneBalanceAfter == userTwoBalanceAfter, "deposit is not additive";
}


// STATUS - verified
// - additivity of withdraw:  withdraw(a); withdraw(b) has same effect as withdraw(a+b)
rule hl_withdrawAdditivity(env e){
    uint256 single; uint256 doubleOne; uint256 doubleTwo;
    require single > 0 && doubleOne > 0 && doubleTwo > 0;
    require single == doubleOne + doubleTwo;

    storage initialStorage = lastStorage;
    withdrawAVAX(e, single);

    uint256 userBalanceAfterSingle = getUserBalance(e.msg.sender);

    withdrawAVAX(e, doubleOne) at initialStorage;
    withdrawAVAX(e, doubleTwo);

    uint256 userBalanceAfterDouble = getUserBalance(e.msg.sender);

    assert userBalanceAfterSingle == userBalanceAfterDouble, "withdraw is not additive";
}


// STATUS - verified
// - deposit and withdraw are two-sided inverses on the state (if successful)
rule hl_twoSideInverse(env e, env e2){
    uint256 amount;
    require getUserBalance(e.msg.sender) > amount;
    require e.msg.sender == e2.msg.sender;  // need two envs because depositAVAX() is payble but withdrawAVAX() isn't, thus, only one e.msg.value causes issues

    storage initialStorage = lastStorage;

    depositAVAX(e);
    withdrawAVAX(e2, amount);
    uint256 balanceOfUser1 = getUserBalance(e.msg.sender);

    withdrawAVAX(e2, amount) at initialStorage;
    depositAVAX(e);
    uint256 balanceOfUser2 = getUserBalance(e.msg.sender);

    assert balanceOfUser1 == balanceOfUser2, "balances are different";
}



// STATUS - verified 
// - no front-running for deposit: effect of deposit unchanged by an intervening operation by another user
rule hl_noDepositFrontRun(method f, env e, env e2){
    require open();
    require e.msg.sender != e2.msg.sender;

    calldataarg args;

    storage initialStorage = lastStorage;

    uint256 userBalanceBefore = getUserBalance(e.msg.sender);
    depositAVAX(e);
    uint256 userBalanceAfter1 = getUserBalance(e.msg.sender);

    f(e2, args) at initialStorage;
    depositAVAX(e);

    uint256 userBalanceAfter2 = getUserBalance(e.msg.sender);

    assert userBalanceBefore + e.msg.value == userBalanceAfter1 && userBalanceBefore + e.msg.value == userBalanceAfter2, "frontrun on Deposit";
}


// STATUS - verified
// - no front-running for withdraw
rule hl_noWithdrawFrontRun(method f, env e, env e2){
    require open();
    require e.msg.sender != e2.msg.sender;
    uint256 amount;
    uint256 userBalanceBefore = getUserBalance(e.msg.sender);
    calldataarg args;

    storage initialStorage = lastStorage;

    f(e2, args);
    withdrawAVAX(e, amount);
    uint256 userBalanceAfter1 = getUserBalance(e.msg.sender);

    withdrawAVAX(e, amount) at initialStorage;
    uint256 userBalanceAfter2 = getUserBalance(e.msg.sender);

    assert userBalanceBefore - amount == userBalanceAfter1 && userBalanceBefore - amount == userBalanceAfter2, "frontrun on Withdraw";
}


// STATUS - verified
// - no front-running for withdrawLiquidity
rule hl_noWithdrawLiquidityFrontRun(method f, env e, env e2){
    require e.msg.sender != e2.msg.sender;
    require e.msg.sender != currentContract;
    require e2.msg.sender != currentContract;
    require closed();
    safeAssumptions(e);

    calldataarg args;

    storage initialStorage = lastStorage;

    uint256 userBalanceBefore = getPairBalance(e.msg.sender);
    uint256 whatShouldGet1 = pairBalance(e, e.msg.sender);
    withdrawLiquidity(e);
    uint256 userBalanceAfter1 = getPairBalance(e.msg.sender);

    f(e2, args) at initialStorage;
    uint256 whatShouldGet2 = pairBalance(e, e.msg.sender);
    withdrawLiquidity(e);
    uint256 userBalanceAfter2 = getPairBalance(e.msg.sender);

    assert whatShouldGet1 == whatShouldGet2, "should get differs";
    assert userBalanceBefore + whatShouldGet1 == userBalanceAfter1 && userBalanceBefore + whatShouldGet2 == userBalanceAfter2, "frontrun on WithdrawLiquidity";
}


// STATUS - verified 
// if stopped then only allowEmergencyWithdraw was called
rule hl_stoppedOnlySwitch(method f, env e){
    require !stopped();

    calldataarg args;
    f(e, args);

    bool isStopped = stopped();

    assert isStopped => f.selector == allowEmergencyWithdraw().selector, "stopped was switch by wrong method";
}


// STATUS - verified 
// allowEmergencyWithdraw only owner call
rule hl_onlyOwnerSwitch(method f, env e){
    require !stopped();

    calldataarg args;
    allowEmergencyWithdraw(e);

    bool isStopped = stopped();

    assert isStopped => e.msg.sender == getOwner(), "stopped was switch by wrong method";
}


// STATUS - verified
// i didn't get a violation: https://vaas-stg.certora.com/output/3106/a422295b5afe610235da/?anonymousKey=724c07c3125626b6659c81fb68f69676260bb6fc
// If event is stopped, appropriate functions will revert
rule hl_whatShouldRevert(method f, env e){
    require stopped();

    calldataarg args;
    f@withrevert(e, args);

    assert((f.selector == depositAVAX().selector
                || f.selector == withdrawAVAX(uint256).selector
                || f.selector == createPair().selector
                || f.selector == withdrawLiquidity().selector)
                => lastReverted, 
                "function was not reverted");
}
