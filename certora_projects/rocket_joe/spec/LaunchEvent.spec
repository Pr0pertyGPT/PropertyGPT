import "./sanity.spec"

using JoeFactory as Factory
using DummyERC20A as SymbERC20A
using DummyERC20B as SymbERC20B
using DummyWeth as Weth

////////////////////////////////////////////////////////////////////////////
//                      Methods                                           //
////////////////////////////////////////////////////////////////////////////

methods {
    // functions
    initialize(address, uint256, address, uint256, uint256, uint256, uint256, uint256, uint256, uint256)
    currentPhase() returns (uint8)
    depositAVAX()
    withdrawAVAX(uint256)
    createPair()
    withdrawLiquidity()
    withdrawIncentives()
    emergencyWithdraw()
    allowEmergencyWithdraw()
    skim()
    getPenalty() returns (uint256)
    getReserves() returns (uint256, uint256)
    getRJoeAmount(uint256) returns (uint256)
    pairBalance(address) returns (uint256)
    _atPhase(uint8)

    // generated getters
    issuer() returns(address) envfree
    auctionStart() returns(uint256) envfree           
    PHASE_ONE_DURATION() returns(uint256) envfree
    PHASE_ONE_NO_FEE_DURATION() returns(uint256) envfree
    PHASE_TWO_DURATION() returns(uint256) envfree
    tokenIncentivesPercent() returns(uint256) envfree
    floorPrice() returns(uint256) envfree
    userTimelock() returns(uint256) envfree
    issuerTimelock() returns(uint256) envfree
    maxWithdrawPenalty() returns(uint256) envfree
    fixedWithdrawPenalty() returns(uint256) envfree
    rJoePerAvax() returns(uint256) envfree
    initialized() returns(bool) envfree
    stopped() returns(bool) envfree
    maxAllocation() returns(uint256) envfree
    WAVAX() returns(address) envfree
    token() returns(address) envfree
    avaxAllocated() returns(uint256) envfree
    pair() returns(address) envfree
    tokenIncentivesBalance() returns(uint256) envfree
    tokenIncentivesForUsers() returns(uint256) envfree
    tokenIncentiveIssuerRefund() returns(uint256) envfree
    lpSupply() returns(uint256) envfree
    tokenReserve() returns(uint256) envfree
    avaxReserve()  returns(uint256) envfree

    // harness functions
    getUserAllocation(address) returns(uint256) envfree
    getUserBalance(address) returns(uint256) envfree
    userHasWithdrawnPair(address) returns(bool) envfree
    userHasWithdrawnIncentives(address) returns(bool) envfree
    getNewWAVAX() returns (address) envfree
    getPenaltyCollector() returns (address) envfree
    getTokenBalanceOfThis() returns (uint256) envfree
    getWAVAXbalanceOfThis() returns (uint256) envfree
    getPairBalanceOfThis() returns (uint256) envfree
    getOwner() returns (address) envfree
    getPairBalance(address) returns (uint256) envfree
    getTokenBalance(address) returns (uint256) envfree
    getPairTotalSupply() returns (uint256) envfree
    getPairTotalSupplyOfThis() returns (uint256) envfree

    isRJLaunchEvent(address) returns(bool) envfree => DISPATCHER(true)
    receiveETH() => DISPATCHER(true)
    
}

////////////////////////////////////////////////////////////////////////////
//                       Definitions                                      //
////////////////////////////////////////////////////////////////////////////


definition NotStarted() returns uint8 = 0;
definition PhaseOne() returns uint8 = 1;
definition PhaseTwo() returns uint8 = 2;
definition PhaseThree() returns uint8 = 3; 

definition oneMinute() returns uint256 = 60;
definition oneHour()   returns uint256 = 60 * oneMinute();
definition oneDay()    returns uint256 = 24 * oneHour();
definition twoDays()    returns uint256 = 2 * oneDay();
definition sevenDays()    returns uint256 = 7 * oneDay();
// definition oneWeek()   returns uint256 = 7  * oneDay();
// definition MAX_DATE()   returns uint256 = 100000000000000000000000000000000000000000000000;
// definition time_bounded(uint256 t) returns bool = t < MAX_DATE() && t > dateOffset();



////////////////////////////////////////////////////////////////////////////
//                         Functions                                      //
////////////////////////////////////////////////////////////////////////////


function helperFunctionsForWithdrawLiquidity(method f, env e) {
	if (f.selector == withdrawLiquidity().selector) {
		withdrawLiquidity(e);
	} else {
        calldataarg args;
        f(e, args);
    }
}


////////////////////////////////////////////////////////////////////////////
//                           Ghosts                                       //
////////////////////////////////////////////////////////////////////////////


ghost sum_of_users_balances() returns uint256 {
    init_state axiom sum_of_users_balances() == 0;
}

hook Sstore getUserInfo[KEY address user].balance uint256 userBalance (uint256 old_userBalance) STORAGE {
    havoc sum_of_users_balances assuming sum_of_users_balances@new() == sum_of_users_balances@old() - old_userBalance + userBalance;
}


// ghost unwithdrawn_users_lp_tokens() returns uint256 {
//     init_state axiom unwithdrawn_users_lp_tokens() == 0;
// }
ghost uint256 unwithdrawn_users_lp_tokens{
    init_state axiom unwithdrawn_users_lp_tokens == 0;
}

hook Sstore getUserPairBalance[KEY address user] uint256 userPairBalance (uint256 old_userPairBalance) STORAGE {
	havoc unwithdrawn_users_lp_tokens assuming unwithdrawn_users_lp_tokens@new == unwithdrawn_users_lp_tokens@old - old_userPairBalance + userPairBalance;
}



////////////////////////////////////////////////////////////////////////////
//                       Invariants                                       //
////////////////////////////////////////////////////////////////////////////



// HELPERS


// STATUS - verified (with harness)
// --rule_sanity failed instate: https://vaas-stg.certora.com/output/3106/2de5b9f58130ede9258d/?anonymousKey=1395a42b2a103b263f982faa8130a8b892f7a1b6
// getPair() should return the same results for both permutations (for current values in the contract)
invariant factoryGetPairCorrelationCurrentVals(env e)
    Factory.getPair(e, token(), WAVAX()) == Factory.getPair(e, WAVAX(), token())
    {
        preserved initialize(address _issuer, uint256 _auctionStart, address _token, uint256 _tokenIncentivesPercent, uint256 _floorPrice, uint256 _maxWithdrawPenalty,
                uint256 _fixedWithdrawPenalty, uint256 _maxAllocation, uint256 _userTimelock, uint256 _issuerTimelock) with (env e2){
            requireInvariant factoryGetPairCorrelationNewVals(e, _token);
        }
    }


// STATUS - verified (with harness)
// getPair() should return the same results for both permutations (for new values that can be assigned in initialize())
invariant factoryGetPairCorrelationNewVals(env e, address token)
    Factory.getPair(e, token, getNewWAVAX()) == Factory.getPair(e, getNewWAVAX(), token)
    {
        preserved initialize(address _issuer, uint256 _auctionStart, address _token, uint256 _tokenIncentivesPercent, uint256 _floorPrice, uint256 _maxWithdrawPenalty,
                uint256 _fixedWithdrawPenalty, uint256 _maxAllocation, uint256 _userTimelock, uint256 _issuerTimelock) with (env e2){
            require token == _token;
        }
    }


// STATUS - verified (with harness)
// -rule_sanity: https://vaas-stg.certora.com/output/3106/c3e711b31a414808a3b3/?anonymousKey=f66a6ec74c47d93a1b72a66ce79cdee30ab9b7ff
// pair and getPair() should return the same adderess
invariant pairAndGetPairCorrelation(env e)
    pair() == Factory.getPair(e, WAVAX(), token())
    {
        preserved{
            requireInvariant isInitialized();
            requireInvariant factoryGetPairCorrelationCurrentVals(e);
        }
    }


// NON INITIALIZED


// STATUS - verified
invariant noIssuerForNonInitialized()
    !initialized() => issuer() == 0

// STATUS - verified
invariant noAllocationIfNonInitialized(address user)
    !initialized() => getUserAllocation(user) == 0

// STATUS - verified
invariant noBalanceIfNonInitialized(address user)
    !initialized() => getUserBalance(user) == 0

// STATUS - in progress. allowEmergencyWithdraw() fails: https://vaas-stg.certora.com/output/3106/f186e56361246ec8fd72/?anonymousKey=f862b3d27b1ace55116959f9788d3e2a6e5d56c1
invariant notStoppedIfNonInitialized()
    !initialized() => !stopped()

// STATUS - 
invariant noAuctionStartIfNonInitialized()
    !initialized() => auctionStart() == 0



// ALWAYS


// STATUS - verified
// - getUI[issuer].allocation == 0
invariant al_issuer_allocation_zero(address user)
    getUserAllocation(issuer()) == 0
    {
        preserved{
            requireInvariant isInitialized();
        }
    }


// STATUS - verified
// - getUI[user].balance <= getUI[user].allocation
invariant al_balance_less_than_allocation(address user)
    getUserBalance(user) <= getUserAllocation(user) 


// STATUS - verified
// - getUI[user].allocation <= maxAllocation
invariant al_userAllocation_less_than_maxAllocation(address user)
    getUserAllocation(user) <= maxAllocation()
    {
        preserved{
            requireInvariant isInitialized();
        }
    }


// // STATUS - verified
// - address(token) != address(wavax)
invariant al_differentTokenAndWavaxAddresses(address user)
    WAVAX() != token()
    {
        preserved initialize(address _issuer, uint256 _auctionStart, address _token, uint256 _tokenIncentivesPercent, uint256 _floorPrice, uint256 _maxWithdrawPenalty,
                uint256 _fixedWithdrawPenalty, uint256 _maxAllocation, uint256 _userTimelock, uint256 _issuerTimelock) with (env e2){
            require getNewWAVAX() != _token;
        }
    }



// INITIALIZED

// STATUS - verified
invariant isInitialized()
    initialized()


// STATUS - in progress. allowEmergencyWithdraw() fails: https://vaas-stg.certora.com/output/3106/c7acf44ab915c9ca241d/?anonymousKey=bf56f5336ce3678bd11250d225cc80089662a446
// - stopped == false
invariant initNotStopped()
    initialized() => !stopped()
    {
        preserved{
            requireInvariant notStoppedIfNonInitialized();
        }
    }


// STATUS - verified
// - `issuerTimelock` >= 1
invariant initIssuerTimelockNonZero()
    initialized() => issuerTimelock() >= 1


// STATUS - verified
// - `userTimelock` <= 7 days
invariant initUserTimelockSeven()
    initialized() => userTimelock() <= sevenDays()


// STATUS - verified
// - `auctionStart` > block.timestamp
invariant initAuctionStart(env e)
    initialized() => auctionStart() > e.block.timestamp
    {
        preserved with (env e2){
            require e.block.timestamp == e2.block.timestamp;
        }
    }


// STATUS - in progress
// in rocketJoeFactory these vars are initialized incorrectly: https://vaas-stg.certora.com/output/3106/7d06eb86e201fe6b2cc4/?anonymousKey=ccddade61f501b5d37192de9f90be6eeafdf25f5
// - `PHASE_ONE_DURATION` == 2 days, `PHASE_ONE_NO_FEE_DURATION` == 1 day, `PHASE_TWO_DURATION` == 1 day
invariant initPhaseTimesSet()
    initialized() => ( PHASE_ONE_DURATION() == twoDays()
            && PHASE_ONE_NO_FEE_DURATION() == oneDay() && PHASE_TWO_DURATION() == oneDay())


// STATUS - verified
//  - `issuerTimelock` > `userTimelock`
invariant initTimelocksCorrelation()
    initialized() => issuerTimelock() > userTimelock()


// STATUS - verified (with invariant that is not finished and with Phases, otherwise createPair() causes a violation(violation as below))
// run: https://vaas-stg.certora.com/output/3106/2ae7324af16683029e39/?anonymousKey=7202818cb360a87ab732a0ccdd7b9b3fa8c34f50
// - `tokenIncentivesForUsers` == `tokenIncentivesBalance`
invariant initIncentivesCorrelation()
    initialized() => tokenIncentivesForUsers() == tokenIncentivesBalance()
    {
        preserved with (env e2){
            requireInvariant initNotStopped();
            require pair() == 0;
            require currentPhase(e2) == NotStarted();
        }
    }


// STATUS - in progress
// run: https://vaas-stg.certora.com/output/3106/9962b89b4833e8ecc445/?anonymousKey=71cbffaf0f4fc093f3f341d5042f1c96547dbabf
// violation in createPair() because incetives go to tokenIncentiveIssuerRefund. State after createPair() is out of the scope of open state
// now also timeout in createPair(): https://vaas-stg.certora.com/output/3106/7f7e33343b63a6ff13c2/?anonymousKey=20fe3b7d573842ad48bfdabc425773a381772003
// violation in depositAVAX() because tool mixes up token and rJoeToken, that's why in burnFrom() rJoeNeeded  subtracted from wrong balance
//  - `tokenReserve` + `tokenIncentivesForUsers` == `token.balanceOf(address(this))`
invariant initTokenBalanceCheck()
    initialized() =>  tokenReserve() + tokenIncentivesForUsers() == getTokenBalanceOfThis()
    {
        preserved with (env e2){
            requireInvariant initNotStopped();
            require pair() == 0;
            require token() == SymbERC20A || token() == SymbERC20B;
            requireInvariant initIncentivesCorrelation();
        }
    }



// OPEN - it's phase one and two. how to combine them? (pair is 0)


// STATUS - in progress 
// violation with allowEmergencyWithdraw()
// open implies not stopped
invariant op_not_stopped()
    pair() == 0 => !stopped()
        // filtered { f -> f.selector != allowEmergencyWithdraw().selector }  // possible bug


// STATUS - verified
// open implies user has not withdrawn
invariant op_user_not_withdrawn_pair(address user)
    pair() == 0 => !userHasWithdrawnPair(user)


// STATUS - verified
// open implies user has not withdrawn
invariant op_user_not_withdrawn_incentives(address user)
    pair() == 0 => !userHasWithdrawnIncentives(user)


// STATUS - in progress
// run: https://vaas-stg.certora.com/output/3106/4287810baacbcf95e993/?anonymousKey=e85517e16f5d7a8c2f2d68cde1b47c6a618e1d00
// state after createPair() is out of the scope of open state
//  - `WAVAX.balanceOf(LaunchEvent)` == Σ getUI[user].balance
invariant opWavaxBalanceAndSumBalances()
    pair() == 0 => getWAVAXbalanceOfThis() == sum_of_users_balances()
    {
        preserved{
            requireInvariant op_not_stopped();                      // double check
            requireInvariant opWavaxBalanceAndWavaxReserve();
        }
    }


// STATUS - in progress
// CreatePair() violation run: https://vaas-stg.certora.com/output/3106/08bc3a2df7c02a6d457d/?anonymousKey=97af371fa551a4fccb66ce7931961aabd180c625
//  - `WAVAX.balanceOf(LaunchEvent)` == `wavaxReserve`
invariant opWavaxBalanceAndWavaxReserve()
    pair() == 0 => getWAVAXbalanceOfThis() == avaxReserve()
    {
        preserved{
            requireInvariant op_not_stopped();
        }
    }


// STATUS - in progress.
// depositAVAX() need token assignment limitation. is it ok?
// Also fails on createPair() but it's out of the scope of this state: https://vaas-stg.certora.com/output/3106/57a31bf01d9d32636b1a/?anonymousKey=582e4dd58c7829bce04c95605cb52089cb73005d
// - token balance of this >= tokenReserve
invariant opTokenBalanceCheck()
    pair() == 0 =>  tokenReserve() + tokenIncentivesForUsers() == getTokenBalanceOfThis()
    {
        preserved with (env e2){
            requireInvariant op_not_stopped();
            require token() == SymbERC20A || token() == SymbERC20B;
            requireInvariant isInitialized();
            requireInvariant initIncentivesCorrelation();
        }
    }  
    

// STATUS - verified
// - avaxAllocated is 0
invariant op_avax_alloc_zero()
    pair() == 0 => avaxAllocated() == 0


// STATUS - verified
//  - lpSupply is 0
invariant op_lp_supply_zero()
    pair() == 0 => lpSupply() == 0


// STATUS - verified
// createPair() violates the property: https://vaas-stg.certora.com/output/3106/6453fa43e1396eb864ad/?anonymousKey=c6322b9a791cdbea942221268091c2c963405500
// - pair.balanceOf(address(this)) == 0
invariant opPairBalanceIsZero()
    pair() == 0 => getPairBalanceOfThis() == 0
    {
        preserved with (env e2){
            requireInvariant pairAndGetPairCorrelation(e2);
            requireInvariant factoryGetPairCorrelationCurrentVals(e2);
        }
    }


// STATUS - verified: https://vaas-stg.certora.com/output/3106/6b7aa9b477a73b95a1d0/?anonymousKey=2a15de91958f4e220f66749b3a67b6fd5886f8ac
// TotalSupply of non-existing pair should be 0 
invariant opPairAndTotalSupplyCorrelation()
    pair() == 0 => getPairTotalSupply() == 0
    {
        preserved with (env e2){
            requireInvariant pairAndGetPairCorrelation(e2);
            requireInvariant factoryGetPairCorrelationCurrentVals(e2);
        }
    }


// STATUS - in progress (createPair() breaks it but it's not a part of this state)
// run of clear rule: https://vaas-stg.certora.com/output/3106/61549927dda329d7423d/?anonymousKey=b30a281f0e63bef766d176d93aff17386e6fbbdf
// run with requires:
invariant op_avax_reserve_sum_user_balances()
     pair() == 0 => avaxReserve() == sum_of_users_balances()



// CLOSED - phase three


// STATUS - in progress (allowEmergencyWithdraw() violation): https://vaas-stg.certora.com/output/3106/eca7dbb4b69c55f85043/?anonymousKey=44a9e39a1f83b15ab36662ee6d898cf1e147e43f
//  - isStopped is false
invariant cl_not_stopped()
    pair() != 0 => !stopped()


// STATUS - verified https://vaas-stg.certora.com/output/3106/0ec29a324e7bdb9f86d2/?anonymousKey=deab759d00c63862d1166abb8a17b91ac040118b
// run without preserved block: https://vaas-stg.certora.com/output/3106/cea4890e65f85e6d14eb/?anonymousKey=94c143aa0c1c85f0f961d154a6e60dafea974945
// run with preserved block: https://vaas-stg.certora.com/output/3106/8863dca9bb0617161eb3/?anonymousKey=14fee042e6c8821f002886c4e7e0861ca072990c
//  - avaxAllocated is Σ getUA[user].balance
invariant cl_avax_alloc_sum_user_balances()
    pair() != 0 => avaxAllocated() == sum_of_users_balances()
    {
        preserved with (env e2){
            requireInvariant cl_not_stopped();                          // emergencyWithdraw()
            require currentPhase(e2) == PhaseThree();                   // withdrawAVAX(uint256) and depositAVAX()
        }
        preserved createPair() with (env e3){
            requireInvariant pairAndGetPairCorrelation(e3);             // createPair()
            requireInvariant factoryGetPairCorrelationCurrentVals(e3);  // createPair()
            require avaxReserve() == sum_of_users_balances();          // Not sure if it's safe
        }
    }


// STATUS - in progress. (need preserved block for createPair() that invariant initially is true like require in a rule)
// run without preserved block: 
// run with preserved block: 
// run: https://vaas-stg.certora.com/output/3106/9d1479ffd6d7489f4c84/?anonymousKey=92f17079fc91748fdd970538af733779da8888c1
invariant clWavaxCorrelation(env e)
    pair() != 0 => (getWAVAXbalanceOfThis() == avaxReserve() && avaxReserve() == 0)
    {
        preserved with (env e2){
            requireInvariant pairAndGetPairCorrelation(e2);
            require currentPhase(e2) == PhaseThree();
        }
    }


// STATUS - in progress
// seems like ghost is wrong: https://vaas-stg.certora.com/output/3106/d1bfde3d7abe7b1e1343/?anonymousKey=853f1b3f34a742b106da974aaed5582c7c373f15
// - pair balance of this = sum of unwithdrawn lp tokens over all users (half to issuers, remainder to users)
// up to roundoff
invariant cl_pair_bal_eq_lp_sum()
    pair() != 0 => (getPairBalanceOfThis() == lpSupply() / 2 + unwithdrawn_users_lp_tokens)
    {
        preserved with (env e2){
            requireInvariant cl_not_stopped();                          // emergencyWithdraw() and skim()
            requireInvariant pairAndGetPairCorrelation(e2);
            requireInvariant opPairBalanceIsZero();
            require token() == SymbERC20A || token() == SymbERC20B;     // withdrawIncentives()
        }
    }


// @AK - I don't understand what do you mean.
//  - token balance of this = sum of unwithdrawn reserve tokens (as above)  // enough incentives to pay everyone 
invariant cl_token_bal_eq_res_token()
    false


// STATUS - in progress
// run without preserved block: https://vaas-stg.certora.com/output/3106/e832cf49cb8c6eb0316a/?anonymousKey=d3e00feecadb1665fc4caf61d0f15b2c60f38459
// run with preserved block (createPair() issue, pre-state pair() == 0 thus we can call this function): https://vaas-stg.certora.com/output/3106/b96d1d489077c95dc026/?anonymousKey=3c4fe014e274f60b7ccc58c12a3b91b558a3e632
// - `tokenIncentivesBalance` <= `tokenIncentivesForUsers`
invariant clIncentivesCorrelation()
    pair() != 0 => (tokenIncentivesBalance() <= tokenIncentivesForUsers())
    {
        preserved with (env e2){
            requireInvariant pairAndGetPairCorrelation(e2);     // createPair()
        }
    }


// STATUS - in progress
// run without preserved block: https://vaas-stg.certora.com/output/3106/00b6f1d898d472549860/?anonymousKey=7231c4055d947eeb860ea21655d5ede46a924804
// run with preserved block (pairBalance() uses wavaxReserve instead of allocation. 
// Seems like it works not correctly because wavaxReserve is not set to 0): https://vaas-stg.certora.com/output/3106/064301bace56d75a880f/?anonymousKey=918b50620df86d27fb24e0f8b24ad162802268c9
//  - user hasWithdrawnPair <=> pair balance of user is nonzero [can be more specific]
invariant cl_nonzero_user_pair_bal(address user, env e)
    pair() != 0 => (!userHasWithdrawnPair(user) <=> pairBalance(e, user) != 0)
    {
        preserved with (env e2){
            requireInvariant cl_not_stopped();                  // emergencyWithdraw()
            require currentPhase(e2) == PhaseThree();           // withdrawAVAX(uint256)
            requireInvariant pairAndGetPairCorrelation(e2);     // createPair()
        }
    }


// STATUS - in progress. 
// run without preserved block: https://vaas-stg.certora.com/output/3106/1f16ef95b837c83df4fa/?anonymousKey=e76a5b8eb2daac59672bb7c219e776d608a4df5d
// run with preserved block: 
//  - WAVAX balance of this is 0
invariant cl_bal_this_zero()
    pair() != 0 => getWAVAXbalanceOfThis() == 0
    {
        preserved with (env e2){
            require currentPhase(e2) == PhaseThree();           // depositAVAX()
            // should I add invariants from open state?
        }
    }





// STOPPED

////////////////////////////////////////////////////////////////////////////
//                       Rules                                            //
////////////////////////////////////////////////////////////////////////////

// STATUS - verified
// this was listed as an invariant, but writing a fixed value property makes more sense as a parametric rule
//  - tokenReserve is fixed (probably nonzero)
rule op_token_res_fixed(method f, env e) {

    require pair() == 0;
    requireInvariant pairAndGetPairCorrelation(e);
    require initialized();
    require !stopped();

    uint256 tokenReserveBefore = tokenReserve();

    calldataarg args;
    f(e, args);

    require pair() == 0;

    uint256 tokenReserveAfter = tokenReserve();

    assert tokenReserveBefore == tokenReserveAfter, "tokenReserve was changed";
}


// STATUS - verified (wirh phase require)
// run of clear rule: https://vaas-stg.certora.com/output/3106/9a14fbfc06f5370a3ff8/?anonymousKey=47be67415c25ce594ca9756c7f1345a2dc65b91b
// run with requires: https://vaas-stg.certora.com/output/3106/c67f41b614e18d7efea7/?anonymousKey=0b1b8ed56327b03298dec62bada231b20c8df0ff
// was listed as an invariant but makes more sense as a parametric rule
//   - getUA[user].allocation is unchanging
rule cl_user_alloc_unchanging(address user, method f, env e) {
    require currentPhase(e) == PhaseThree(); // depositAVAX()

    uint256 userAllocationBefore = getUserAllocation(user);

    calldataarg args;
    f(e, args);

    uint256 userAllocationAfter = getUserAllocation(user);

    assert userAllocationBefore == userAllocationAfter, "tokenReserve was changed";
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  - avaxAllocated, tokenAllocated, lpSupply, tokenReserve are unchanging
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// STATUS - in progress (createPair has pair == 0 OR totalSupply == 0 - it's the issue)
// can require pair.totalSupply > 0; it should fix the issue
// run of clear rule: https://vaas-stg.certora.com/output/3106/6069ba941c41dddb93d0/?anonymousKey=ff0feaa921181f9619053106c79339e70e6c68a4
// run with requires: https://vaas-stg.certora.com/output/3106/a505898e420fa73c6f46/?anonymousKey=4e20fb5ac95682f53cfbe50ffc848f11c151a5b9
rule cl_avax_alloc_fixed(method f, env e) {
    require pair() != 0;
    requireInvariant pairAndGetPairCorrelation(e);

    uint256 wavaxAllocatedBefore = avaxAllocated();

    calldataarg args;
    f(e, args);

    uint256 wavaxAllocatedAfter = avaxAllocated();

    assert wavaxAllocatedBefore == wavaxAllocatedAfter, "not yet implemented";
}

// STATUS - in progress (the same issue as above)
// run of clear rule: https://vaas-stg.certora.com/output/3106/3a0c7c688b06022747cf/?anonymousKey=b77728a94b1d226a2beec6070cf021b13673db34
// run with requires: https://vaas-stg.certora.com/output/3106/97f94a4070310e71fcc6/?anonymousKey=886fa365aa4a2a5f32009b54a816d1f5d1c8afe5
rule cl_lp_supply_fixed(method f, env e) {
    require pair() != 0;
    requireInvariant pairAndGetPairCorrelation(e);

    uint256 lpSupplyBefore = lpSupply();

    calldataarg args;
    f(e, args);

    uint256 lpSupplyAfter = lpSupply();

    assert lpSupplyBefore == lpSupplyAfter, "not yet implemented";
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Variable changes
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////


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


// STATUS - in progress (strange sanity again deposit and withdraw AVAX: https://vaas-stg.certora.com/output/3106/bc15b3b66210ce04bde5/?anonymousKey=4b3ae52a5a992806a04a2314ab5c560cdc3ffd3d)
// - getUI[user].balance only changed by user in deposit and withdraw (see method specs)
rule op_balanceChangeByDepositOrWithdraw(method f, env e){     
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
    require pair() == 0;                    // createPair() and withdrawLiquidity()
    requireInvariant pairAndGetPairCorrelation(e);   // createPair()
    requireInvariant opPairAndTotalSupplyCorrelation();     // createPair()
    requireInvariant op_not_stopped();      // emergencyWithdraw()
    requireInvariant isInitialized();       // initialize()

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
    require pair() == 0;                    // withdrawIncentives()
    requireInvariant op_not_stopped();      // emergencyWithdraw()
    requireInvariant isInitialized();       // initialize()

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
    require pair() == 0;                    // createPair()
    requireInvariant pairAndGetPairCorrelation(e);   // createPair()
    requireInvariant opPairAndTotalSupplyCorrelation();     // createPair()
    requireInvariant isInitialized();       // initialize()

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
rule op_tokenIncentiveIssuerRefundUnchange(method f, env e){
    require pair() == 0;                                    // createPair()
    requireInvariant pairAndGetPairCorrelation(e);          // createPair()
    requireInvariant opPairAndTotalSupplyCorrelation();     // createPair()

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
    requireInvariant pairAndGetPairCorrelation(e);

    address pairBefore = pair();

    calldataarg args;
    f(e, args);

    address pairAfter = pair();

    assert pairBefore != pairAfter <=> f.selector == createPair().selector, "pair was changed by wrong method";
}


// STATUS - verified
rule tr_initializedOnlyChange(method f){     
    bool initBefore = initialized();

    env e;
    calldataarg args;
    f(e, args);

    bool initAfter = initialized();

    assert initBefore != initAfter <=> f.selector == initialize(address, uint256, address, uint256, uint256, uint256, uint256, uint256, uint256, uint256).selector, "initialized was changed by wrong method";
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
    require pair() != 0;
    requireInvariant pairAndGetPairCorrelation(e);

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
    require pair() != 0;                                // createPair()
    requireInvariant pairAndGetPairCorrelation(e);      // createPair()
    requireInvariant isInitialized();                   // initialize()
    require currentPhase(e) == PhaseThree();            // depositAVAX() 


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
    require initialized();
    // require pair() != 0;
    // require pair() == Factory.getPair(e, WAVAX(), token());

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
    require initialized();          // initialize()

    uint256 tokenIncentivesBalanceBefore = tokenIncentivesBalance();

    require tokenIncentivesBalanceBefore > 0;

    calldataarg args;
    f(e, args);

    uint256 tokenIncentivesBalanceAfter = tokenIncentivesBalance();

    assert tokenIncentivesBalanceAfter == 0 <=> f.selector == emergencyWithdraw().selector, "tokenIncentivesBalance is 0 unintentionally";
}



/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// High-level rules
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// STATUS - in progress (check correctness, how to write a ghost)
// - pair balance of this == pair balance of issuer + Σ pair balance of user  == pair.totalSupply
invariant hl_EqualityOfPairs()
    getPairBalanceOfThis() == getPairBalance(issuer()) + sumOfPairBalances()


// STATUS - in progress
// run without preserved block: https://vaas-stg.certora.com/output/3106/1f91c36ac4e4424e389f/?anonymousKey=c30c7ee9fd1cb8fe7198145cf50a5e0959f623e4
// run with preserved block: 
invariant hl_EqualityOfPairAndTotalSupply()
    getPairBalanceOfThis() == getPairTotalSupplyOfThis()


// STATUS - in progress
// run without preserved block: https://vaas-stg.certora.com/output/3106/23f2a4a600d0a020f0cb/?anonymousKey=d1d4fef9e201e201fd039a0dd0ddc1ea5306c9d7
// run with preserved block: https://vaas-stg.certora.com/output/3106/9a888396ade18f00c01a/?anonymousKey=a7cdb01cf4b007d42ee8c2eb885757bfeebef6e6
invariant hl_TotalSupplyEquality()
    getPairTotalSupply() == getPairTotalSupplyOfThis()
    {
        preserved with (env e2){
            requireInvariant factoryGetPairCorrelationCurrentVals(e2);
            // requireInvariant factoryGetPairCorrelationNewVals(e2);
            requireInvariant pairAndGetPairCorrelation(e2);
            require Weth != currentContract;
        }
    }


// STATUS - in progress (check correctness)
// run without preserved block: https://vaas-stg.certora.com/output/3106/97ef875729677fd13d3e/?anonymousKey=2de9f81c045b5e5905703a7e1858051c83398e3c
// run with preserved block: https://vaas-stg.certora.com/output/3106/fd13b3facc56fe203493/?anonymousKey=215dd5bd8dea94c48915359907e365dafbeee0c1
// - token balance of this == tokenReserve + tokenIncentivesBalance
// don't see if loop for withdrawLiquidity()
// strange call trace for emergencyWithdraw()
invariant hl_EqualityOfToken(env e) 
    getTokenBalanceOfThis() == tokenReserve() + tokenIncentivesBalance()
    {
        preserved with (env e2){
            require token() == SymbERC20A || token() == SymbERC20B;     // depositAVAX() and many more          // token != instead of ==
            require e2.msg.sender != currentContract;                   // withdrawIncentives()
            require e.msg.sender == e2.msg.sender;       
            // require e2.msg.sender == issuer();               
        }
    }


// STATUS - in progress
// run of clear rule: https://vaas-stg.certora.com/output/3106/f4bc7ac13d8eb2bd3a0a/?anonymousKey=8f7ad6b696892571f8fd47f715a541e782849805
// run with requires:
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

    uint256 userBalanceAtStart = getUserBalance(e.msg.sender);

    storage initialStorage = lastStorage;
    withdrawAVAX(e, single);

    uint256 userBalanceAfterSingle = getUserBalance(e.msg.sender);

    withdrawAVAX(e, doubleOne) at initialStorage;
    withdrawAVAX(e, doubleTwo);

    uint256 userBalanceAfterDouble = getUserBalance(e.msg.sender);

    assert userBalanceAfterSingle == userBalanceAfterDouble, "withdraw is not additive";
}


// STATUS - in progress
// values are set in a way that pairBalance() returns 0: https://vaas-stg.certora.com/output/3106/8d248960ef13f105b235/?anonymousKey=8a2c40d9e5369140c4fae50b8a9705cef9b5bde4
// in withdrawIncentives() pair and token are mixed up by dispatcher (instead of token, pair transfer is used) that's why pairBalance was increased
// why was token balance increased too?
// run: https://vaas-stg.certora.com/output/3106/c1f832414d46105ad050/?anonymousKey=76fee1c34e2a9c4f7192143d89e967335e2f73c5
// maybe avaxAllocated() should be set correctly
// run: https://vaas-stg.certora.com/output/3106/0f95076ff69d2b551578/?anonymousKey=212ef1e0e250849feac6ffb6421768c745899ace
// maybe incentives too
// - if I deposit more AVAX, I receive more LP and launch tokens

// define formula for depositin in order to get more
rule hl_moreDepositMoreGet(method f, env e, env e2){
    require e.msg.sender != e2.msg.sender;
    require e.msg.sender != issuer();
    require e2.msg.sender != issuer();
    require e.msg.sender != currentContract;
    require e2.msg.sender != currentContract;
    require lpSupply() >= avaxAllocated(); // assumption, need to double check
    require token() == SymbERC20A || token() == SymbERC20B;

    uint256 balanceOfuser1 = getUserBalance(e.msg.sender);
    uint256 balanceOfuser2 = getUserBalance(e2.msg.sender);
    require balanceOfuser2 > balanceOfuser1;
    require avaxAllocated() >= balanceOfuser2 + balanceOfuser1;

    uint256 pairOfuser1Before = getPairBalance(e.msg.sender);
    uint256 tokenOfuser1Before = getTokenBalance(e.msg.sender);

    uint256 pairOfuser2Before = getPairBalance(e2.msg.sender);
    uint256 tokenOfuser2Before = getTokenBalance(e2.msg.sender);

    require pairOfuser1Before == pairOfuser2Before;
    require tokenOfuser1Before == tokenOfuser2Before;

    withdrawLiquidity(e);
    withdrawIncentives(e);
    // check how much can I withdrawLiquidity or how much I withdrawn
    uint256 pairOfuser1After = getPairBalance(e.msg.sender);
    // check how much can I withdrawIncentives or how much I withdrawn
    uint256 tokenOfuser1After = getTokenBalance(e.msg.sender);

    withdrawLiquidity(e2);
    withdrawIncentives(e2);
    // check how much can I withdrawLiquidity or how much I withdrawn
    uint256 pairOfuser2After = getPairBalance(e2.msg.sender);
    // check how much can I withdrawIncentives or how much I withdrawn
    uint256 tokenOfuser2After = getTokenBalance(e2.msg.sender);

    //assert
    assert pairOfuser1After < pairOfuser2After && tokenOfuser1After < tokenOfuser2After, "more deposit doesn't guarantee more rewards";
}


// STATUS - in progress
// need to play with setup: https://vaas-stg.certora.com/output/3106/7dbf520e634a88f8f53d/?anonymousKey=f1f9b5601b6ba73425a4c3389ef0408e658ba972
// - if I withdraw AVAX later, I have a larger penalty
rule hl_withdrawLateMorePenalty(method f, env e, env e2){
    // define phase 1, the second half

    require auctionStart() < e.block.timestamp;
    require e.block.timestamp < e2.block.timestamp;
    require e.block.timestamp > oneDay() && e.block.timestamp < twoDays();
    require e2.block.timestamp < twoDays();

    require e.msg.sender == e2.msg.sender;
    require e.msg.sender != issuer();
    require e.msg.sender != currentContract;

    uint256 earlyPenalty = getPenalty(e);
    uint256 latePenalty = getPenalty(e2);

    assert earlyPenalty < latePenalty, "penalty isn't greater";
}


// STATUS - verified
// run of clear rule: 
// run with requires: 
// do I need to check for non-reverting? 
// - deposit and withdraw are two-sided inverses on the state (if successful)
rule hl_twoSideInverse(env e){
    uint256 amount;

    storage initialStorage = lastStorage;

    depositAVAX(e);
    withdrawAVAX(e, amount);
    uint256 balanceOfUser1 = getUserBalance(e.msg.sender);

    withdrawAVAX(e, amount) at initialStorage;
    depositAVAX(e);
    uint256 balanceOfUser2 = getUserBalance(e.msg.sender);

    assert balanceOfUser1 == balanceOfUser2, "balances are different";
}


// STATUS - verified. --rule_sanity fails on 2 methods: https://vaas-stg.certora.com/output/3106/aa1385e04d4954850309/?anonymousKey=12d1ecc17e5ad4ad9ca4dd2803136d0897ff898e 
// - no front-running for deposit: effect of deposit unchanged by an intervening operation by another user
rule hl_noDepositFrontRun(method f, env e, env e2){
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


// STATUS - verified (assume the same as above)
// - no front-running for withdraw
rule hl_noWithdrawFrontRun(method f, env e, env e2){
    require e.msg.sender != e2.msg.sender;
    uint256 amount;

    calldataarg args;

    storage initialStorage = lastStorage;

    uint256 userBalanceBefore = getUserBalance(e.msg.sender);
    withdrawAVAX(e, amount);
    uint256 userBalanceAfter1 = getUserBalance(e.msg.sender);

    f(e2, args) at initialStorage;
    withdrawAVAX(e, amount);

    uint256 userBalanceAfter2 = getUserBalance(e.msg.sender);

    assert userBalanceBefore - amount == userBalanceAfter1 && userBalanceBefore - amount == userBalanceAfter2, "frontrun on Withdraw";
}


// STATUS - in progress. 
// Need phases. run: https://vaas-stg.certora.com/output/3106/b5504d1e06207a552948/?anonymousKey=465bcaf38ba6e5b1d88a97b655413542c853d014
// - no front-running for withdrawLiquidity
rule hl_noWithdrawLiquidityFrontRun(method f, env e, env e2){
    require e.msg.sender != e2.msg.sender;
    require e.msg.sender != currentContract;
    require e2.msg.sender != currentContract;

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


// - createPair can be called at least once (DoS check)
// no front running for create pair
rule hl_createPairAtLeastOnce(env e){
    require !stopped();

    // storage

    createPair(e);

    // storage


    assert !lastReverted, "createPair DoS";
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Unit tests
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
