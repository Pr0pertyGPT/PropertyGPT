import "./LEValidStates.spec"

use invariant alwaysInitialized
use invariant oneStateOnly
use invariant factoryGetPairCorrelationCurrentVals
use invariant al_issuer_allocation_zero
use invariant al_balance_less_than_allocation
use invariant al_userAllocation_less_than_maxAllocation
use invariant initIssuerTimelockNonZero
use invariant initUserTimelockSeven
use invariant initTimelocksCorrelation
use invariant op_incentivesCorrelation
use invariant op_user_not_withdrawn_pair
use invariant op_user_not_withdrawn_incentives
use invariant opWavaxBalanceAndSumBalances
use invariant op_avax_alloc_zero
use invariant op_lp_supply_zero
use invariant opPairBalanceIsZero
// use invariant opPairAndTotalSupplyCorrelation
// use invariant cl_pairTotalZero
use invariant cl_avax_alloc_sum_user_balances
use invariant cl_avaxReservCheck
// use invariant cl_PhaseCheck
// use invariant cl_AvaxCorrelation
// use invariant cl_pair_bal_eq_lp_sum
// use invariant cl_incentivesCorrelation
// use invariant cl_nonzero_user_pair_bal
// use invariant cl_bal_this_zero
use invariant cl_pairAndGetPairCorrelation


// ALWAYS


// STATUS - verified
// - user allocation cannot be decreased
rule al_userAllocationNonDecreasing(method f, env e){     
    address user;

    uint256 allocationBefore = getUserAllocation(user);

    calldataarg args;
    f(e, args);

    uint256 allocationAfter = getUserAllocation(user);

    assert allocationBefore <= allocationAfter, "allocation was decreased";
}


// STATUS - verified (strange sanity with deposit and withdraw AVAX: https://vaas-stg.certora.com/output/3106/c81af4162d3207acc467/?anonymousKey=bd70c1a61143b991a8027ec2ad3d319417d060cd)
// - isStopped only changed by owner
rule al_stoppedOnlyByOwner(method f, env e){
    bool isStoppedBefore = stopped();

    calldataarg args;
    f(e, args);

    bool isStoppedAfter = stopped();

    assert isStoppedBefore != isStoppedAfter => (e.msg.sender == getOwner() && isStoppedBefore == false), "pair was changed by wrong method";
}


// OPEN


// STATUS - verified
// sanity issue: https://vaas-stg.certora.com/output/3106/803f0d0b53975ac8efca/?anonymousKey=2715cb118d2185eca7c96916ccdbce86009da2db
// - getUI[user].balance only changed by user in deposit and withdraw (see method specs)
rule op_balanceChangeByDepositOrWithdraw(method f, env e){     
    require open();
    
    address user;
    uint256 balanceBefore = getUserBalance(user);

    calldataarg args;
    f(e, args);

    uint256 balanceAfter = getUserBalance(user);

    assert balanceBefore != balanceAfter <=> (e.msg.sender == user && (f.selector == depositAVAX().selector || f.selector == withdrawAVAX(uint256).selector)), "pair was changed by wrong method";
}


// STATUS - verified
// - getUI[user].allocation only changed by user in deposit (see method specs)
rule op_allocationChangeByDeposit(method f, env e){
    address user;

    uint256 allocationBefore = getUserAllocation(user);

    calldataarg args;
    f(e, args);

    uint256 allocationAfter = getUserAllocation(user);

    assert allocationBefore != allocationAfter => (f.selector == depositAVAX().selector && e.msg.sender == user), "allocation was changed by wrong method";
}

// STATUS - verified
// run of clear rule: https://vaas-stg.certora.com/output/3106/4b9d5dacb4e4196177a5/?anonymousKey=dbb76cc8610527f3339807de214cd6b9dbb358a3
// run with requires: https://vaas-stg.certora.com/output/3106/0ac33a29f30c6644f35e/?anonymousKey=91a997ff0a506811488b71e5b52a7d9f8874b935
// - `tokenReserve` is unchanging
rule op_tokenReserveUnchange(method f, env e){

    uint256 tokenReserveBefore = tokenReserve();

    calldataarg args;
    f(e, args);

    uint256 tokenReserveAfter = tokenReserve();

    assert tokenReserveBefore == tokenReserveAfter, "tokenReserve was changed";
}

// STATUS - verified
// run of clear rule: https://vaas-stg.certora.com/output/3106/3cceb76eee67c0ed1e5b/?anonymousKey=e1009fdefca94a64cbd1c7bbff21164345bccebe
// run with requires: https://vaas-stg.certora.com/output/3106/c699ff5c5be3fbef1861/?anonymousKey=47eb62af13b8a4505f8fbbb213e31480caa0404e
// - `tokenIncentivesBalance` is unchanging
rule op_tokenIncentivesBalanceUnchange(method f, env e){

    uint256 tokenIncentivesBalanceBefore = tokenIncentivesBalance();

    calldataarg args;
    f(e, args);

    uint256 tokenIncentivesBalanceAfter = tokenIncentivesBalance();

    assert tokenIncentivesBalanceBefore == tokenIncentivesBalanceAfter, "tokenIncentivesBalance was changed";
}

// STATUS - verified
// run of clear rule: https://vaas-stg.certora.com/output/3106/040d0a8ed6d70c1f47d2/?anonymousKey=f0b8e025f93740e372b9b1c1f498521aea8824c8
// run with requires: https://vaas-stg.certora.com/output/3106/c47a11d2ce4c6a14be09/?anonymousKey=54b4657ee6216dcc865048773ab193a481d91b1c
// - `tokenIncentivesForUsers` is unchanging
rule op_tokenIncentivesForUsersUnchange(method f, env e){

    uint256 tokenIncentivesForUsersBefore = tokenIncentivesForUsers();

    calldataarg args;
    f(e, args);

    uint256 tokenIncentivesForUsersAfter = tokenIncentivesForUsers();

    assert tokenIncentivesForUsersBefore == tokenIncentivesForUsersAfter, "tokenRestokenIncentivesForUserserve was changed";
}

// STATUS - verified
// run of clear rule: https://vaas-stg.certora.com/output/3106/ce28f43ca464d99b6d6a/?anonymousKey=9bad700e78b9b7b33110f37a414d45accdcfc698
// run with requires: https://vaas-stg.certora.com/output/3106/856420e40afee720de4e/?anonymousKey=c62d3855f1b6acdbf588674c9ee7135f46d3e81e
// - `tokenIncentiveIssuerRefund` is unchanging
rule op_tokenIncentiveIssuerRefundUnchange(method f, env e){// createPair()

    uint256 tokenIncentiveIssuerRefundBefore = tokenIncentiveIssuerRefund();

    calldataarg args;
    f(e, args);

    uint256 tokenIncentiveIssuerRefundAfter = tokenIncentiveIssuerRefund();

    assert tokenIncentiveIssuerRefundBefore == tokenIncentiveIssuerRefundAfter, "tokenIncentiveIssuerRefund was changed";
}







// TRANSITION: OPEN -> CLOSED


// STATUS - in progress (change require to requireInvariant once it's ready)
// strange --rule_sanity result for depositAVAX() method: https://vaas-stg.certora.com/output/3106/d6762c5bb403e67ce0c2/?anonymousKey=56ead439f7ea597631a317ddb619731d671c0673
// the same with assert sanity in code: https://vaas-stg.certora.com/output/3106/469882c2854db4873da6/?anonymousKey=5c0b79adb59e36322c3f22de5a9e37ee7329af30
// run of clear rule: https://vaas-stg.certora.com/output/3106/7755f3cba04e571e87d8/?anonymousKey=7aa2f72db908be0282d2b9e5f08dd53d82c0513b
// run with requires: https://vaas-stg.certora.com/output/3106/fe2a0a0a63bf759a67c1/?anonymousKey=bb597b279b979745058a8b85c40e56a41e585455
// maybe it's not correct that pair should change in createPair()
rule tr_pairOnlyChange(method f, env e){     

    address pairBefore = pair();

    calldataarg args;
    f(e, args);

    address pairAfter = pair();

    assert pairBefore != pairAfter <=> f.selector == createPair().selector, "pair was changed by wrong method";
}


// STATUS - verified
rule tr_initializedOnlyChange(method f){     
    uint256 initBefore = auctionStart();

    env e;
    calldataarg args;
    f(e, args);

    uint256 initAfter = auctionStart();

    assert initBefore != initAfter <=> (initBefore == 0 && f.selector == initialize(address, uint256, address, uint256, uint256, uint256, uint256, uint256, uint256, uint256).selector), "initialized was changed by wrong method";
}


// STATUS - verified ("=>" instead of "<=>" because it may not be changed)
rule tr_incentivesForUsersChanges(method f){     
    uint256 incentivesBefore = tokenIncentivesForUsers();

    env e;
    calldataarg args;
    f(e, args);

    uint256 incentivesAfter = tokenIncentivesForUsers();

    assert incentivesBefore != incentivesAfter 
                => f.selector == initialize(address, uint256, address, uint256, uint256, uint256, uint256, uint256, uint256, uint256).selector
                || f.selector == createPair().selector, "tokenIncentivesForUsers was changed by wrong method";
}


// STATUS - verified ("=>" instead of "<=>" because it may not be changed if "if" in createPair() wasn't executed)
rule tr_incentiveIssuerRefundChanges(method f){     
    uint256 incentivesBefore = tokenIncentiveIssuerRefund();

    env e;
    calldataarg args;
    f(e, args);

    uint256 incentivesAfter = tokenIncentiveIssuerRefund();

    assert incentivesBefore != incentivesAfter => f.selector == createPair().selector, "tokenIncentiveIssuerRefund was changed by wrong method";
}






// CLOSED


// STATUS - verified
// - pair is unchanging
rule cl_unchangingPair(method f, env e){

    address pairBefore = pair();

    calldataarg args;
    f(e, args);

    address pairAfter = pair();

    assert pairBefore == pairAfter, "pair was changed in close stage";
}


// invariant cl_wavaxNotZero()
//     pair() != 0 => avaxAllocated() > 0

// STATUS - in progress (maybe add userHasWithdrawnPair(issuer()) => tokenReserve() == 0) - does => <=> make sense?
// run without preserved block: https://vaas-stg.certora.com/output/3106/b0f4853713af2301edcb/?anonymousKey=ea101ebc4801f04d91fddc5053dd7f37425a8089
// run with preserved block: 
// - hasWithdrawnPair and LP token balance of user are related
// invariant cl_hasWithdrawnPair_and_pairBalance_Correlation(env e, address user)
//     pair() != 0 => (userHasWithdrawnPair(user) <=> getPairBalance(user) == pairBalance(e, user))
//     {
//         preserved{
//             requireInvariant cl_wavaxNotZero();
//         }
//     }


// STATUS - verified
// run of clear rule: https://vaas-stg.certora.com/output/3106/1a5e11364b6e8c28969e/?anonymousKey=204b54ee5d57842688899fea38f27428dbc62f5a
// run with requires: https://vaas-stg.certora.com/output/3106/2ebb3102ee4febf309fe/?anonymousKey=54b4aee885636a0e19d2d32f5692d3818b9899e7
// - hasWithdrawnPair and LP token balance change only in withdrawLiquidity
// - hasWithdrawnPair and LP token balance of user are related
rule cl_hasWithdrawnPair_pairBalance_OnlyChangeUser(method f, env e){
    address user;
    require user != currentContract;
    require user == e.msg.sender;
    require user != issuer();

    bool hasWPairBefore = userHasWithdrawnPair(user);
    uint256 userPairBalanceBefore = getPairBalance(user);
    uint256 possiblePairBalance = pairBalance(e, user);

    helperFunctionsForWithdrawLiquidity(f, e);
    
    bool hasWPairAfter = userHasWithdrawnPair(user);
    uint256 userPairBalanceAfter = getPairBalance(user);

    assert (hasWPairBefore != hasWPairAfter && userPairBalanceAfter == userPairBalanceBefore + possiblePairBalance) <=> f.selector == withdrawLiquidity().selector, "hasWithdrawnPair was changed by wrong method";
}

// STATUS - verified
rule cl_hasWithdrawnPair_pairBalance_OnlyChangeIssuer(method f, env e){
    address user;
    require user != currentContract;
    require user == e.msg.sender;
    require user == issuer();
    require token() == SymbERC20A || token() == SymbERC20B;

    bool hasWPairBefore = userHasWithdrawnPair(user);
    uint256 userPairBalanceBefore = getPairBalance(user);

    helperFunctionsForWithdrawLiquidity(f, e);
    
    bool hasWPairAfter = userHasWithdrawnPair(user);
    uint256 userPairBalanceAfter = getPairBalance(user);

    assert (hasWPairBefore != hasWPairAfter && userPairBalanceAfter == userPairBalanceBefore + (lpSupply() / 2)) <=> f.selector == withdrawLiquidity().selector, "hasWithdrawnPair was changed by wrong method";
}


// STATUS - in progress
// run of clear rule: https://vaas-stg.certora.com/output/3106/88a43abaa5d01d354cb9/?anonymousKey=aaa145502fc37e129e5fb22516a5a596f247f1c7
// run with requires (createPair() can be called for the second time 
// (because totalBalance == 0). it causes violation): https://vaas-stg.certora.com/output/3106/cbba8a84f218d35d76e0/?anonymousKey=41ddb51a318fbfcdc2b0d224f5c055e632ba890f
// - LP and launch token balance of LaunchEvent are decreasing
rule cl_pairAndTokenBalancesNonIncreasing(method f, env e){          
    uint256 tokenBalanceBefore = getTokenBalanceOfThis();
    uint256 pairBalanceBefore = getPairBalanceOfThis();

    calldataarg args;
    f(e, args);

    uint256 tokenBalanceAfter = getTokenBalanceOfThis();
    uint256 pairBalanceAfter = getPairBalanceOfThis();

    assert tokenBalanceBefore >= tokenBalanceAfter, "token balance was increased";
    assert pairBalanceBefore >= pairBalanceAfter, "pair balance was increased";
}


// STATUS - verified
// - user.hasWithdrawnIncentives changes only in `withdrawIncentives` (see method spec)
rule cl_hasWithdrawnIncentivesOnlyChange(method f, env e){
    bool hasWIncenBefore = userHasWithdrawnIncentives(e.msg.sender);

    calldataarg args;
    f(e, args);

    bool hasWIncenAfter = userHasWithdrawnIncentives(e.msg.sender);

    assert hasWIncenBefore != hasWIncenAfter => f.selector == withdrawIncentives().selector, "hasWithdrawnIncentives was changed by wrong method";
}


// STATUS - verified
// run of clear rule: https://vaas-stg.certora.com/output/3106/9a374505cb8a7717f883/?anonymousKey=24813bf0f90c13d48cb99e653d511cb1298815fc
// run with requires: https://vaas-stg.certora.com/output/3106/117db959388ea6161147/?anonymousKey=bebe9014aced19c204572942b2c2dd85c7bcb23a
// - tokenIncentivesBalance is non-increasing
rule cl_tokenIncentivesBalancesNonIncreasing(method f, env e){
    requireInvariant alwaysInitialized();

    uint256 tokenIncentivesBalanceBefore = tokenIncentivesBalance();

    calldataarg args;
    f(e, args);

    uint256 tokenIncentivesBalanceAfter = tokenIncentivesBalance();

    assert tokenIncentivesBalanceBefore >= tokenIncentivesBalanceAfter, "token incentives balance was increased";
}


// STATUS - in progress. !!!!!!!!!!!! Need a ghost to track unwithdrawn incentives !!!!!!
// run of clear rule: https://vaas-stg.certora.com/output/3106/6cc68dbdc10b2695404d/?anonymousKey=886ca0f9674adbf620407c088fa5b71c47624438
// run with requires:
// - tokenIncentivesBalance can be 0 only if emergencyWithdraw() was called or all users withdrawn their incentives (need ghost - idk how to do it)
rule cl_tokenIncentivesBalanceCanBeZero(method f, env e){
    requireInvariant alwaysInitialized();   

    uint256 tokenIncentivesBalanceBefore = tokenIncentivesBalance();

    require tokenIncentivesBalanceBefore > 0;

    calldataarg args;
    f(e, args);

    uint256 tokenIncentivesBalanceAfter = tokenIncentivesBalance();

    assert tokenIncentivesBalanceAfter == 0 <=> f.selector == emergencyWithdraw().selector, "tokenIncentivesBalance is 0 unintentionally";
}
