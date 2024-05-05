import "./sanity.spec"

using JoeFactory as Factory
using DummyERC20A as SymbERC20A
using DummyERC20B as SymbERC20B
using DummyWeth as Weth
using JoePair as JP
using RocketJoeToken as RJT

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
    getIncentives(address) returns (uint256)

    // generated getters
    issuer() returns(address) envfree
    auctionStart() returns(uint256) envfree           
    tokenIncentivesPercent() returns(uint256) envfree
    floorPrice() returns(uint256) envfree
    userTimelock() returns(uint256) envfree
    issuerTimelock() returns(uint256) envfree
    maxWithdrawPenalty() returns(uint256) envfree
    fixedWithdrawPenalty() returns(uint256) envfree
    rJoePerAvax() returns(uint256) envfree
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
    avaxReserve() returns(uint256) envfree
    tokenAllocated() returns(uint256) envfree
    rJoe() returns(address) envfree
    phaseOneDuration() returns(uint256) envfree
    phaseOneNoFeeDuration() returns(uint256) envfree
    phaseTwoDuration() returns(uint256) envfree

    // harness functions
    getUserAllocation(address) returns(uint256) envfree
    getUserBalance(address) returns(uint256) envfree
    userHasWithdrawnPair(address) returns(bool) envfree
    userHasWithdrawnIncentives(address) returns(bool) envfree
    getNewWAVAX() returns (address) envfree
    getPenaltyCollector() returns (address) envfree
    getTokenBalanceOfThis() returns (uint256) envfree
    getWAVAXbalanceOfThis() returns (uint256) envfree
    getWAVAXbalanceOfPair() returns (uint256) envfree
    getPairBalanceOfThis() returns (uint256) envfree
    getOwner() returns (address) envfree
    getPairBalance(address) returns (uint256) envfree
    getTokenBalance(address) returns (uint256) envfree
    getPairTotalSupply() returns (uint256) envfree
    getPairTotalSupplyOfThis() returns (uint256) envfree
    getBalanceOfThis() returns (uint256) envfree
    factoryGetPairWT() returns (address) envfree
    factoryGetPairTW() returns (address) envfree
 
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



definition open() returns bool =
    pair() == 0 && !stopped();

definition closed() returns bool =
    pair() != 0 && !stopped();

definition openStopped() returns bool =
    pair() == 0 && stopped();

definition closedStopped() returns bool =
    pair() != 0 && stopped();


invariant oneStateOnly()
    open() && !closed() && !openStopped() && !closedStopped() ||
    !open() && closed() && !openStopped() && !closedStopped() ||
    !open() && !closed() && openStopped() && !closedStopped() ||
    !open() && !closed() && !openStopped() && closedStopped()


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


function revertFunctions(method f, env e) {
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
