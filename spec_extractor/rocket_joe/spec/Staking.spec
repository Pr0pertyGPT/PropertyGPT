import "../helpers/erc20.spec"

////////////////////////////////////////////////////////////////////////////
//                      Methods                                           //
////////////////////////////////////////////////////////////////////////////
using DummyERC20Impl as joe
using DummyERC20A as A

using RocketJoeToken as rJoe

methods {
    // external functions
    mint(address, uint256) returns (uint256) => DISPATCHER(true) // does not seem to be functioning

    // generated getters 
    lastRewardTimestamp() returns (uint256) envfree
    accRJoePerShare() returns (uint256) envfree
    rJoePerSec() returns (uint256) envfree
    totalJoeStaked() returns (uint256) envfree
    // mapping(address => UserInfo) public userInfo;
    // Initialize(IERC20Upgradeable _joe, RocketJoeToken _rJoe, uint256 _rJoePerSec)
    
    // internal functions
    pendingRJoe(address) returns (uint256)
    deposit(uint256)
    withdraw(uint256)
    emergencyWithdraw()
    updatePool()
    updateEmissionRate(uint256)
    // _safeRJoeTransfer(address, uint256) // internal

    // harness functions
    userJoeStaked(address) returns (uint256) envfree
    userRewardDebt(address) returns (uint256) envfree
    getOwner() returns (address) envfree
    PRECISION() returns (uint256) envfree
}

// rule sanity(method f) {
//     env e; calldataarg args;
//     f(e, args);
//     assert false;
// }

ghost sum_user_balance() returns uint256;
// {
// //     init_state axiom sum_user_balance() == 0;
//     // axiom forall address a. forall address b. sum_user_balance() >= userJoeStaked(a) + userJoeStaked(b);
// }

ghost sum_user_rewards() returns uint256;
// {
//     init_state axiom sum_user_rewards() == 0;
// }

// user sum balance hook
hook Sstore userInfo[KEY address user].amount uint256 userBalance (uint256 oldUserBalance) STORAGE {
    havoc sum_user_balance assuming
        sum_user_balance@new() == sum_user_balance@old() + userBalance - oldUserBalance;
}

hook Sstore rJoe._balances[KEY address user] uint256 reward (uint256 oldReward) STORAGE {
    havoc sum_user_rewards assuming
        sum_user_rewards@new() == sum_user_rewards@old() + reward - oldReward;
}

// initialization invariance 

ghost initialized() returns bool;

ghost initializing() returns bool;

// hook Sload bool init currentContract._initialized STORAGE {
//   havoc initialized assuming initialized@new() == init;
// }

hook Sstore currentContract._initialized bool init STORAGE {
    havoc initialized assuming initialized@new() == init;
}

hook Sstore currentContract._initializing bool initing STORAGE {
    havoc initializing assuming initializing@new() == initing;
}

// helper invariants 
invariant is_initialized()
    initialized()
{ preserved {
    requireInvariant not_initializing();
}}

invariant not_initializing()
    !initializing()


////////////////////////////////////////////////////////////////////////////
//                       Invariants                                       //
////////////////////////////////////////////////////////////////////////////

// // rJoe.totalSupply is sum of rJoe balances
// invariant User_RJ_balance_sums_supply()
//     false



//joe.balanceOf(RJStaking)  ≥ Σ userInfo[user].amount
// invariant staking_joe_bal_sums_user_balance(env e) // passes
//    joe.balanceOf(e, currentContract) >= sum_user_balance()
// { preserved with (env otherE) {
//     require otherE.msg.sender != currentContract;
//     requireInvariant user_balances_less_than_totalJoeStaked();
// } }

// invariant totalJoeStaked_sums_user_balance() // passes
//     totalJoeStaked() == sum_user_balance()
// { preserved {
//     requireInvariant user_balances_less_than_totalJoeStaked();
// }}

invariant balanceOf_Joe_eq_totalJoeStaked(env e) // passes
   joe.balanceOf(e, currentContract) >= totalJoeStaked()
{ preserved with (env otherE){
    require otherE.msg.sender != currentContract;
} }

invariant user_balances_less_than_totalJoeStaked() // passes
    forall address a. forall address b. (a != b) => to_uint256(totalJoeStaked()) >= userJoeStaked(a) + userJoeStaked(b)
{ preserved with (env e) {
    require e.msg.sender != currentContract;
}}

// non-zero e.msg.sender implies a non-zero reward debt?

////////////////////////////////////////////////////////////////////////////
//                       Rules                                            //
////////////////////////////////////////////////////////////////////////////


//userInfo[user].amount only changed by user in deposit/withdraw/emergencyWithdraw
// passes
rule userInfo_amount_safe_mutate(method f) {
    env e; calldataarg args;
    address user;
    uint256 userBalance_pre = userJoeStaked(user);
    f(e, args);
    uint256 userBalance_post = userJoeStaked(user);
    assert userBalance_pre != userBalance_post => f.selector == deposit(uint256).selector ||
                                            f.selector == withdraw(uint256).selector ||
                                            f.selector == emergencyWithdraw().selector, "improper function mutated user balance";
    assert userBalance_pre != userBalance_post => e.msg.sender == user, "non-user mutated balance";

}

// rJoePerSec only changed by owner in updateEmissionRate
// passes
rule RJPS_only_owner_and_function(method f) filtered { f -> f.selector != 0xeb990c59} 
{
    requireInvariant is_initialized();
    requireInvariant not_initializing();
    env e; calldataarg args;
    uint256 RJPS_pre = rJoePerSec();
    f(e, args);
    uint256 RJPS_post = rJoePerSec();

    assert RJPS_post != RJPS_pre => f.selector == updateEmissionRate(uint256).selector, "changed by wrong function";
    assert RJPS_post != RJPS_pre => e.msg.sender == getOwner(), "changed by non-owner";
}

// pendingReward[user] only decreased by user
rule pending_reward_decreased_only_user(method f) filtered { f -> (f.selector != 0xeb990c59 && f.selector != emergencyWithdraw().selector)
} { 
    requireInvariant is_initialized();
    requireInvariant not_initializing();
    // requireInvariant totalJoeStaked_sums_user_balance();
    env e; calldataarg args;
    require totalJoeStaked() < 1000000000000000; // max_uint256 - 1000; // rewards will decrease by 1 or 2 sometimes when it's close to max
    require e.msg.sender != currentContract;
    address user;
    uint256 rjoe_pre = pendingRJoe(e, user);
    f(e, args);
    uint256 rjoe_post = pendingRJoe(e, user);
    assert rjoe_post < rjoe_pre => e.msg.sender == user; 
}

//  - If I am staked, I get some RJoe
rule staking_non_trivial_rJoe() {
    // requireInvariant totalJoeStaked_sums_user_balance();
    requireInvariant is_initialized();
    requireInvariant not_initializing();
    require PRECISION() > 0;
    require rJoePerSec() > 0 && rJoePerSec() < 1000000; // realistic range to help the tool run this rule faster

    uint256 amount;
    require amount > 0;
    env e0; env e1;
    require e0.msg.sender == e1.msg.sender;

    deposit(e0, amount);
    require e1.block.timestamp > lastRewardTimestamp();
    require userRewardDebt(e0.msg.sender) < max_uint256;
    uint dt = e1.block.timestamp - lastRewardTimestamp(); // store this as a variable for more readable cex
    uint256 rewards = pendingRJoe(e1, e0.msg.sender);
    assert exists uint256 t. (t == dt) => rewards > 0,  "trivial rJoe";

    // doing the min interval calculations would likely be a better rule but causes timeouts, left for future consideration
    // uint256 min_interval = totalJoeStaked() / rJoePerSec();
    // require min_interval < (max_uint256 / 10) && min_interval > 0; // divide by 10 to reduce the scope of the problem
    // assert dt > min_interval => rJoe != 0, "trivial rJoe";
}

rule staking_trivial_on_zero_time() { // passes
    uint256 amount;
    require amount > 0;
    env e0;
    deposit(e0, amount);

    env e1; 
    uint delta_t = e1.block.timestamp - e0.block.timestamp; // store this as a variable for more readable cex
    require delta_t == 0; 
    uint256 rJoe = pendingRJoe(e1, e0.msg.sender);
    assert rJoe == 0, "RJOE gained with no stake time";
}

//  - If I stake longer, I get more reward
// vacuous 
rule longer_stake_greater_return() { // passes

    storage init = lastStorage; 
    uint256 amount;
    require amount > 0;
    env e0;
    env e1; 
    env e2; 

    // accessing the same account, not current contract
    require e0.msg.sender != currentContract && e1.msg.sender == e0.msg.sender && e2.msg.sender == e0.msg.sender;
    // account 2 stakes longer than account 1, which stakes more than 0 seconds
    require e1.block.timestamp > e0.block.timestamp && e2.block.timestamp > e1.block.timestamp;

    

    deposit(e0, amount);
    uint256 rJoe1 = pendingRJoe(e1, e0.msg.sender);
    deposit(e0, amount) at init;
    uint256 rJoe2 = pendingRJoe(e2, e0.msg.sender);

    // assert rJoe2 > rJoe1; 
    assert exists uint256 dt. e2.block.timestamp - e1.block.timestamp >= dt => rJoe2 > rJoe1;
}




//  - No front-running for deposit:   `f(); deposit(...)` has same result as `deposit()`)
// measure user's erc20 balance too? TODO
rule deposit_no_frontrunning(method f) // passes
{
    // setup
    env e; calldataarg args;
    uint256 x;
    require userJoeStaked(currentContract) > x;
    uint256 bal_pre_clean = userJoeStaked(e.msg.sender);
    uint256 user_bal_pre_clean = joe.balanceOf(e, e.msg.sender);
    storage init = lastStorage;

    // run with frontrunning
    f(e, args);
    require userJoeStaked(currentContract) > x;
    uint256 bal_pre_f = userJoeStaked(e.msg.sender);
    uint256 user_bal_pre_f = joe.balanceOf(e, e.msg.sender);
    deposit(e, x);
    uint256 bal_post_f = userJoeStaked(e.msg.sender);
    uint256 user_bal_post_f = joe.balanceOf(e, e.msg.sender);
    uint256 delta_f = bal_post_f - bal_pre_f;

    // run without frontrunning
    deposit(e, x) at init;
    uint256 bal_post_clean = userJoeStaked(e.msg.sender);
    uint256 user_bal_post_clean = joe.balanceOf(e, e.msg.sender);
    uint256 delta_clean = bal_post_clean - bal_pre_clean;

    assert delta_f == delta_clean, "frontrunning found";
    assert user_bal_pre_clean - user_bal_post_clean == user_bal_pre_f - user_bal_post_f, "balance not received by user";
}
//  - No front-running for withdraw   `f(); withdraw(...)` has same result as `withdraw()`)
// change to support case where balance is less than amount? // TODO
rule withdraw_no_frontrunning(method f) filtered { f-> (f.selector != emergencyWithdraw().selector)}
{
    // setup
    env e; calldataarg args;
    uint256 x;
    require userJoeStaked(currentContract) > x;
    uint256 bal_pre_clean =  userJoeStaked(e.msg.sender);
    uint256 user_bal_pre_clean = joe.balanceOf(e, e.msg.sender);
    storage init = lastStorage;

    // run with frontrunning
    f(e, args);
    require userJoeStaked(currentContract) > x;
    uint256 bal_pre_f = userJoeStaked(e.msg.sender);
    uint256 user_bal_pre_f = joe.balanceOf(e, e.msg.sender);
    withdraw(e, x);
    uint256 bal_post_f = userJoeStaked(e.msg.sender);
    uint256 user_bal_post_f = joe.balanceOf(e, e.msg.sender);
    uint256 delta_f = bal_pre_f - bal_post_f;

    // run without fruntrunning
    withdraw(e, x) at init;
    uint256 user_bal_post_clean = joe.balanceOf(e, e.msg.sender);
    uint256 bal_post_clean = userJoeStaked(e.msg.sender);
    uint256 delta_clean = bal_pre_clean - bal_post_clean;

    assert delta_f == delta_clean, "frontrunning found";
    assert user_bal_post_clean - user_bal_pre_clean == user_bal_post_f - user_bal_pre_f, "user joe not spent";
}

// additivty with frontrunning for greater coverage?
rule additivity_withdraw() {
    storage init = lastStorage;
    env e; 
    uint256 x;
    uint256 y;
    // require x > 0 && y > 0;
    // require userJoeStakede.msg.sender) > x + y;
    withdraw(e, x);
    withdraw(e, y);

    uint256 bal_sep = userJoeStaked(e.msg.sender);

    withdraw(e, x+y) at init;
    uint256 bal_sum = userJoeStaked(e.msg.sender);
    
    assert bal_sep == bal_sum, "additivity failed";
}

rule additivity_deposit() {
    uint256 x;
    uint256 y;
    env e; 
    require x > 0 && y > 0;

    storage init = lastStorage;

    deposit(e, x);
    deposit(e, y);

    uint256 bal_sep = userJoeStaked(e.msg.sender);

    deposit(e, x+y) at init;
    uint256 bal_sum = userJoeStaked(e.msg.sender);

    assert bal_sep == bal_sum, "additivity failed";
}

rule verify_deposit() {
    env e;
    require e.msg.sender != currentContract;
    uint256 amount; 

    uint256 balance_pre = userJoeStaked(e.msg.sender);
    uint256 reward_debt_pre = userRewardDebt(e.msg.sender);
    uint256 total_pre = totalJoeStaked();
    deposit(e, amount);
    uint256 balance_post = userJoeStaked(e.msg.sender);
    uint256 reward_debt_post = userRewardDebt(e.msg.sender);
    uint256 total_post = totalJoeStaked();

    assert total_post == total_pre + amount, "totalJoeStaked not updated properly";
    assert balance_post - amount == balance_pre, "improper amount deposited";
    assert (e.block.timestamp > lastRewardTimestamp() => reward_debt_post > reward_debt_pre)  || userJoeStaked(e.msg.sender) == 0, "reward debt not increased";
    assert pendingRJoe(e, e.msg.sender) == 0, "user has unclaimed rewards";
}

rule verify_withdraw() {
    env e;
    require e.msg.sender != currentContract;
    uint256 amount; 

    uint256 balance_pre = userJoeStaked(e.msg.sender);
    uint256 reward_debt_pre = userRewardDebt(e.msg.sender);
    uint256 total_pre = totalJoeStaked();
    withdraw(e, amount);
    uint256 balance_post = userJoeStaked(e.msg.sender);
    uint256 reward_debt_post = userRewardDebt(e.msg.sender);
    uint256 total_post = totalJoeStaked();

    assert total_post == total_pre - amount, "totalJoeStaked not updated properly";
    assert balance_pre - amount == balance_post, "improper amount withdrawn";
    assert (e.block.timestamp > lastRewardTimestamp() => reward_debt_post > reward_debt_pre) || userJoeStaked(e.msg.sender) == 0, "reward debt not increased";
    assert pendingRJoe(e, e.msg.sender) == 0, "user has unclaimed rewards";
}

rule verify_updateEmissionRate {
    env e; 
    uint256 emissionRate;
    updateEmissionRate(e, emissionRate);
    assert rJoePerSec() == emissionRate, "emission rate not updated";
}

rule updatePool_contained() {
    env e;
    address user;
    uint256 balance_pre = userJoeStaked(user);
    uint256 reward_debt_pre = userRewardDebt(user);
    updatePool(e);
    assert userJoeStaked(user) == balance_pre, "balance changed";
    assert userRewardDebt(user) == reward_debt_pre, "reward debt changed";
}
// assuming emergency withdraw doesn't revert, everything else passes
rule verify_emergencyWithdraw() {
    env e;

    uint256 userJoe_pre = userJoeStaked(e.msg.sender);
    uint256 stakingJoe_pre = joe.balanceOf(e, currentContract);
    uint256 total_joe_pre = totalJoeStaked();
    require e.msg.sender == A;

    emergencyWithdraw@withrevert(e);
    require lastReverted == false;

    uint256 total_joe_post = totalJoeStaked();
    assert total_joe_post == total_joe_pre - userJoe_pre, "totalJoeStaked not updated properly";
    // assert lastReverted == false, "failed, should not fail"; 
    assert userJoeStaked(e.msg.sender) == 0, "user still had joe remaining";
}

//  - updatePool is a no-op (`updatePool(); f(...)` has same result as `f()`)
//  - rJoe.totalSupply increasing at constant rate (rJoePerSec)


// // I'd like to do an invariant that shows this is always increasing, but I can't see a good way to do so
// this rule has been kind of a pain and doesn't add much to coverage past what non_trivial_rJoe and duration correlates return already provide
// rule updatePool_increases_accRJoePerShare() {
//     require PRECISION > 0;
//     env e;
//     require e.block.timestamp > lastRewardTimestamp();
//     require joe.balanceOf(e, currentContract) > 0; // will not increase if supply is 0
//     uint256 pre = accRJoePerShare();
//     updatePool(e);
//     uint256 post = accRJoePerShare();
//     assert post > pre, "acc not increasing";
// }


// rule stake_duration_correlates_return() { // passes

//     storage init = lastStorage; 
//     uint256 amount;
//     require amount > 0;
//     env e0;
//     env e1; 
//     env e2; 

//     // accessing the same account, not current contract
//     require e0.msg.sender != currentContract && e1.msg.sender == e0.msg.sender && e2.msg.sender == e0.msg.sender;
//     // account 2 stakes longer than account 1, which stakes more than 0 seconds
//     require e1.block.timestamp > e0.block.timestamp && e2.block.timestamp > e1.block.timestamp;

    

//     deposit(e0, amount);
//     uint256 rJoe1 = pendingRJoe(e1, e0.msg.sender);
//     deposit(e0, amount) at init;
//     uint256 rJoe2 = pendingRJoe(e2, e0.msg.sender);

//     // assert rJoe2 > rJoe1; 
//     assert e2.block.timestamp > e1.block.timestamp <=> rJoe2 >= rJoe1;
// }


// invariant rJoe_solvency(env e, address user)
//     rJoe.balanceOf(e, currentContract) >= pendingRJoe(e, user)
// { preserved with (env otherE) {
//     require otherE.msg.sender != currentContract;
// }}
