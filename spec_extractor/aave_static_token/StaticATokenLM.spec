import "erc20.spec"

using AToken as _AToken 
using RewardsControllerHarness as _RewardsController 
using DummyERC20_aTokenUnderlying as _DummyERC20_aTokenUnderlying 
using DummyERC20_rewardToken as _DummyERC20_rewardToken 
using SymbolicLendingPoolL1 as _SymbolicLendingPoolL1 
using TransferStrategyHarness as _TransferStrategy
using StaticATokenLMHarness as _StaticATokenLM
using ScaledBalanceTokenHarness as _ScaledBalanceToken

methods
{

    totalSupply() returns uint256 envfree
	balanceOf(address) returns (uint256) envfree
    rewardTokens() returns (address[]) envfree

    getRewardTokensLength() returns (uint256) envfree 
    getRewardToken(uint256) returns (address) envfree
    isRegisteredRewardToken(address) envfree

    _AToken.totalSupply() returns uint256 envfree
	_AToken.balanceOf(address) returns (uint256) envfree
	_AToken.scaledTotalSupply() returns (uint256) envfree
    _AToken.scaledBalanceOf(address) returns (uint256) envfree
    _AToken.transferFrom(address,address,uint256) returns (bool)
    
    _RewardsController.getAvailableRewardsCount(address) returns (uint128) envfree
    _RewardsController.getDistributionEnd(address, address)  returns (uint256) envfree
    _RewardsController.getRewardsByAsset(address,uint128) returns (address ) envfree
    _RewardsController.getUserAccruedRewards(address, address) returns (uint256) envfree
    _RewardsController.getAssetByIndex(uint256) returns (address) envfree
    _RewardsController.getAssetListLength() returns (uint256) envfree
    _RewardsController.getUserAccruedReward(address, address, address) returns (uint256) envfree
    _RewardsController.getAssetDecimals(address) returns (uint8) envfree 
    _RewardsController.getRewardsData(address,address) returns (uint256,uint256,uint256,uint256) envfree
    _RewardsController.getUserAssetIndex(address,address, address) returns (uint256) envfree 
    
    _DummyERC20_rewardToken.balanceOf(address) returns (uint256) envfree

    /*******************
    *     Pool.sol     *
    ********************/

    //getReserveNormalizedIncome(address) returns (uint256) => ALWAYS(1000000000000000000000000000)

    //Called by RewardsController.sol
    //Defined in RewardsDistributor.sol
    getAssetIndex(address, address) returns (uint256, uint256) =>  DISPATCHER(true)
    
    //Called by AToken.sol
    //Defined in SupplyLogic.sol
    finalizeTransfer(address, address, address, uint256, uint256, uint256) => NONDET  

    //Called by getAssetIndex
    // Defined in ScaledBalanceTokenBase.sol
    scaledTotalSupply() returns (uint256) envfree => DISPATCHER(true) 
    

   /*****************************
    *     OZ ERC20Permit.sol     *
    ******************************/
    permit(address,address,uint256,uint256,uint8,bytes32,bytes32) => NONDET

    /*********************
    *     AToken.sol     *
    **********************/
    mint(address,address,uint256,uint256) returns (bool) => DISPATCHER(true)
    burn(address,address,uint256,uint256) returns (bool) => DISPATCHER(true)
    getIncentivesController() returns (address) => CONSTANT
    UNDERLYING_ASSET_ADDRESS() returns (address) => CONSTANT
    
    /**********************************
    *     RewardsDistributor.sol     *
    **********************************/
    getRewardsList() returns (address[]) => NONDET

    /**********************************
    *     RewardsController.sol     *
    **********************************/

    //Called by IncentivizedERC20.sol and by StaticATokenLM.sol
    handleAction(address,uint256,uint256) => DISPATCHER(true)

    //Called by RewardsController.sol
    //Defined in ScaledBalanceTokenBase.sol
    getScaledUserBalanceAndSupply(address) returns (uint256, uint256) => DISPATCHER(true)

    //Called by RewardsController._transferRewards()
    //Defined in TransferStrategyHarness as simple transfer() 
    performTransfer(address,address,uint256) returns (bool) =>  DISPATCHER(true)

 }

/// @title Claim rewards methods
definition claimFunctions(method f) returns bool = 
            f.selector == claimRewardsToSelf(address[]).selector ||
            f.selector == claimRewards(address, address[]).selector ||
            f.selector ==claimRewardsOnBehalf(address, address,address[]).selector ||
            f.selector == collectAndUpdateRewards(address).selector;



// /// @title Reward hook
// /// @notice allows a single reward
// /// @dev todo: hook may be omitted
// hook Sload address reward _rewardTokens[INDEX  uint256 i] STORAGE {
//    require reward == _DummyERC20_rewardToken;
// } 


/// @title Sum of balances of StaticATokenLM 
ghost sumAllBalance() returns mathint {
    init_state axiom sumAllBalance() == 0;
}

hook Sstore balanceOf[KEY address a] uint256 balance (uint256 old_balance) STORAGE {
  havoc sumAllBalance assuming sumAllBalance@new() == sumAllBalance@old() + balance - old_balance;
}

hook Sload uint256 balance balanceOf[KEY address a] STORAGE {
    require balance <= sumAllBalance();
} 

/// @title Sum of scaled balances of AToken 
ghost sumAllATokenScaledBalance() returns mathint {
    init_state axiom sumAllATokenScaledBalance() == 0;
}

hook Sstore _AToken._userState[KEY address a] .(offset 0) uint128 balance (uint128 old_balance) STORAGE {
  havoc sumAllATokenScaledBalance assuming sumAllATokenScaledBalance@new() == sumAllATokenScaledBalance@old() + balance - old_balance;
}

hook Sload uint128 balance _AToken._userState[KEY address a] .(offset 0) STORAGE {
    require balance <= sumAllATokenScaledBalance();
} 


/// @title Static AToeknLM balancerOf(user) <= totalSupply()
invariant inv_balanceOf_leq_totalSupply(address user)
	balanceOf(user) <= totalSupply()
	{
		preserved {
			requireInvariant sumAllBalance_eq_totalSupply();
		}
	}

/// @title AToken balancerOf(user) <= AToken totalSupply()
//timeout on redeem metaWithdraw
invariant inv_atoken_balanceOf_leq_totalSupply(address user)
	_AToken.balanceOf(user) <= _AToken.totalSupply()
     filtered { f -> !f.isView && f.selector != redeem(uint256,address,address,bool).selector}
    {
		preserved with (env e){
			requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
        }
	}

/// @title AToken balancerOf(user) <= AToken totalSupply()
/// @dev case split of inv_atoken_balanceOf_leq_totalSupply
invariant inv_atoken_balanceOf_leq_totalSupply_redeem(address user)
	_AToken.balanceOf(user) <= _AToken.totalSupply()
    filtered { f -> f.selector == redeem(uint256,address,address,bool).selector}
    {
		preserved with (env e){
			requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
    	}
	}

/// @title AToken sum of 2 balancers <= AToken totalSupply()
invariant inv_atoken_balanceOf_2users_leq_totalSupply(address user1, address user2)
	(_AToken.balanceOf(user1) + _AToken.balanceOf(user2))<= _AToken.totalSupply()
    {
		preserved with (env e1){
            setup(e1, user1);
		    setup(e1, user2);
		}
        preserved redeem(uint256 shares, address receiver, address owner) with (env e2){
            require user1 != user2;
            require _AToken.balanceOf(currentContract) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
        }
        preserved redeem(uint256 shares, address receiver, address owner, bool toUnderlying) with (env e3){
            require user1 != user2;
        	requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
            require _AToken.balanceOf(e3.msg.sender) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
            require _AToken.balanceOf(currentContract) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
        }
        preserved withdraw(uint256 assets, address receiver,address owner) with (env e4){
            require user1 != user2;
        	requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
            require _AToken.balanceOf(e4.msg.sender) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
            require _AToken.balanceOf(currentContract) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
        }

        preserved metaWithdraw(address owner, address recipient,uint256 staticAmount,uint256 dynamicAmount,bool toUnderlying,uint256 deadline,_StaticATokenLM.SignatureParams sigParams)
        with (env e5){
            require user1 != user2;
        	requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
            require _AToken.balanceOf(e5.msg.sender) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
            require _AToken.balanceOf(currentContract) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
        }

	}

/// @title AToken scaledBalancerOf(user) <= AToken scaledTotalSupply()
invariant inv_atoken_scaled_balanceOf_leq_totalSupply(address user)
	_AToken.scaledBalanceOf(user) <= _AToken.scaledTotalSupply()
    {
		preserved {
			requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
		}
	}

/// @title Sum of balances=totalSupply()
invariant sumAllBalance_eq_totalSupply()
	sumAllBalance() == totalSupply()

/// @title Sum of AToken scaled balances = AToken scaled totalSupply()
invariant sumAllATokenScaledBalance_eq_totalSupply()
	sumAllATokenScaledBalance() == _AToken.scaledTotalSupply()



/// @title Assumptions that should hold in any run
/// @dev Assume that the memory was configured by calling RewardsController.configureAssets(RewardsDataTypes.RewardsConfigInput[] memory rewardsInput) 
function setup(env e, address user)
{
    
    //assume a single reward
    require getRewardTokensLength() == 1;
    require getRewardToken(0) == _DummyERC20_rewardToken;

    require _RewardsController.getAvailableRewardsCount(_AToken)  > 0;
    require _RewardsController.getRewardsByAsset(_AToken, 0) == _DummyERC20_rewardToken;

    require currentContract != e.msg.sender;
    require _AToken != e.msg.sender;
    require _RewardsController != e.msg.sender;
    require _DummyERC20_aTokenUnderlying  != e.msg.sender;
    require _DummyERC20_rewardToken != e.msg.sender;
    require _SymbolicLendingPoolL1 != e.msg.sender;
    require _TransferStrategy != e.msg.sender;
    require _ScaledBalanceToken != e.msg.sender;
    require _TransferStrategy != e.msg.sender;
   

    require currentContract != user;
    require _AToken != user;
    require _RewardsController !=  user;
    require _DummyERC20_aTokenUnderlying  != user;
    require _DummyERC20_rewardToken != user;
    require _SymbolicLendingPoolL1 != user;
    require _TransferStrategy != user;
    require _ScaledBalanceToken != user;
    require _TransferStrategy != user;
}

//pass
/// @title correct accrued value is fetched
/// @notice assume a single asset
invariant singleAssetAccruedRewards(env e0, address asset, address reward, address user)
    ((_RewardsController.getAssetListLength() == 1 && _RewardsController.getAssetByIndex(0) == asset)
        => (_RewardsController.getUserAccruedReward(asset, reward, user) == _RewardsController.getUserAccruedRewards(reward, user)))
        {
            preserved with (env e1){
                setup(e1, user);
                require asset != _RewardsController;
                require asset != _TransferStrategy;
                require asset != _ScaledBalanceToken;
                require reward != _StaticATokenLM;
                require reward != _AToken;
                require reward != _ScaledBalanceToken;
                require reward != _TransferStrategy;
            }
        }


//pass
/// @title Claiming rewards should not affect totalAssets() 
rule totalAssets_stable(method f)
    filtered { f -> (f.selector == claimRewardsToSelf(address[]).selector ||
                    f.selector == claimRewards(address, address[]).selector ||
                    f.selector == claimRewardsOnBehalf(address, address,address[]).selector) }
{
    env e;
    calldataarg args;
    mathint totalAssetBefore = totalAssets(e);
    f(e, args); 
    mathint totalAssetAfter = totalAssets(e);
    assert totalAssetAfter == totalAssetBefore;
}

//pass
/// @title Claiming rewards should not affect totalAssets() 
/// @dev case splitting
rule totalAssets_stable_after_collectAndUpdateRewards()
{
    env e;
    require _RewardsController.getRewardsByAsset(_AToken, 0) != _AToken;
    require _RewardsController.getUserAccruedReward(currentContract, _AToken, _AToken) ==0;
    address reward;
    mathint totalAssetBefore = totalAssets(e);
    collectAndUpdateRewards(e, reward); 
    mathint totalAssetAfter = totalAssets(e);
    assert totalAssetAfter == totalAssetBefore;
}


//pass
/// @title Receiving ATokens does not affect the amount of rewards fetched by collectAndUpdateRewards()
rule reward_balance_stable_after_collectAndUpdateRewards()
{
    env e;
    address reward;
    address sender;
    uint256 amount;

    storage initial = lastStorage;
    collectAndUpdateRewards(e, reward); 
    mathint reward_balance_before = _DummyERC20_rewardToken.balanceOf(currentContract);

    _AToken.transferFrom(e, sender, currentContract, amount) at initial;
    collectAndUpdateRewards(e, reward); 
    mathint reward_balance_after = _DummyERC20_rewardToken.balanceOf(currentContract);

    assert reward_balance_before == reward_balance_after;
}

// timeout on mint, redeem, deposit, withdraw
/// @title getTotalClaimableRewards() is stable unless rewards were claimed
rule totalClaimableRewards_stable(method f)
    filtered { f -> !f.isView && !claimFunctions(f)  && f.selector != initialize(address,string,string).selector  }
{
    env e;
    require e.msg.sender != currentContract;
    setup(e, 0);
    calldataarg args;
    address reward;
    require e.msg.sender != reward;
    require currentContract != e.msg.sender;
    require _AToken != e.msg.sender;
    require _RewardsController != e.msg.sender;
    require _DummyERC20_aTokenUnderlying  != e.msg.sender;
    require _DummyERC20_rewardToken != e.msg.sender;
    require _SymbolicLendingPoolL1 != e.msg.sender;
    require _TransferStrategy != e.msg.sender;
    require _ScaledBalanceToken != e.msg.sender;
    require _TransferStrategy != e.msg.sender;

    require currentContract != reward;
    require _AToken != reward;
    require _RewardsController !=  reward;
    require _DummyERC20_aTokenUnderlying  != reward;
    require _SymbolicLendingPoolL1 != reward;
    require _TransferStrategy != reward;
    require _ScaledBalanceToken != reward;
    require _TransferStrategy != reward;


    mathint totalClaimableRewardsBefore = getTotalClaimableRewards(e, reward);
    f(e, args); 
    mathint totalClaimableRewardsAfter = getTotalClaimableRewards(e, reward);
    assert totalClaimableRewardsAfter == totalClaimableRewardsBefore;
}


//should fail
//timeout
rule totalClaimableRewards_stable_SANITY(method f)
    filtered { f -> f.selector == claimSingleRewardOnBehalf(address, address,address).selector   }
{
    env e;
    require e.msg.sender != currentContract;
    setup(e, 0);
    calldataarg args;
    address reward;
    require e.msg.sender != reward;
    require currentContract != e.msg.sender;
    require _AToken != e.msg.sender;
    require _RewardsController != e.msg.sender;
    require _DummyERC20_aTokenUnderlying  != e.msg.sender;
    require _DummyERC20_rewardToken != e.msg.sender;
    require _SymbolicLendingPoolL1 != e.msg.sender;
    require _TransferStrategy != e.msg.sender;
    require _ScaledBalanceToken != e.msg.sender;
    require _TransferStrategy != e.msg.sender;

    require currentContract != reward;
    require _AToken != reward;
    require _RewardsController !=  reward;
    require _DummyERC20_aTokenUnderlying  != reward;
    require _SymbolicLendingPoolL1 != reward;
    require _TransferStrategy != reward;
    require _ScaledBalanceToken != reward;
    require _TransferStrategy != reward;


    mathint totalClaimableRewardsBefore = getTotalClaimableRewards(e, reward);
    f(e, args); 
    mathint totalClaimableRewardsAfter = getTotalClaimableRewards(e, reward);
    assert totalClaimableRewardsAfter == totalClaimableRewardsBefore;
}


//fail
//https://vaas-stg.certora.com/output/99352/ba0861e8dc5041798c08c829609172dd/?anonymousKey=7cea930ea4c17235e0c56ca78bd50bc58207ae07
//https://vaas-stg.certora.com/output/99352/fd3b2507ac5546b4b1155c95ddeebb56/?anonymousKey=3ad66ba03ecfaf49d9c0258e60b8f4ef47a24e16
/// @title getTotalClaimableRewards() is stable after initialized()
rule totalClaimableRewards_stable_after_initialized()
{
    env e;
    require e.msg.sender != currentContract;
    setup(e, 0);
    calldataarg args;
    address reward;


    require e.msg.sender != reward;
 
    require currentContract != e.msg.sender;
    require _AToken != e.msg.sender;
    require _RewardsController != e.msg.sender;
    require _DummyERC20_aTokenUnderlying  != e.msg.sender;
    require _DummyERC20_rewardToken != e.msg.sender;
    require _SymbolicLendingPoolL1 != e.msg.sender;
    require _TransferStrategy != e.msg.sender;
    require _ScaledBalanceToken != e.msg.sender;
    require _TransferStrategy != e.msg.sender;

    require currentContract != reward;
    require _AToken != reward;
    require _RewardsController !=  reward;
    require _DummyERC20_aTokenUnderlying  != reward;
    require _SymbolicLendingPoolL1 != reward;
    require _TransferStrategy != reward;
    require _ScaledBalanceToken != reward;
    require _TransferStrategy != reward;

    address newAToken;
    string staticATokenName;
    string staticATokenSymbol;

    mathint totalClaimableRewardsBefore = getTotalClaimableRewards(e, reward);
    initialize(e, newAToken, staticATokenName, staticATokenSymbol);
    mathint totalClaimableRewardsAfter = getTotalClaimableRewards(e, reward);
    assert totalClaimableRewardsAfter == totalClaimableRewardsBefore;
}


//pass 
/// @title getClaimableRewards() is stable unless rewards were claimed
rule getClaimableRewards_stable(method f)
    filtered { f -> !f.isView
                    && !claimFunctions(f)
                    && f.selector != initialize(address,string,string).selector
                    && f.selector != deposit(uint256,address,uint16,bool).selector
    }
{
    env e;
    calldataarg args;
    address user;
    address reward;
    
    require user != 0;

    setup(e, user);    
    //assume a single reward
    require reward == _DummyERC20_rewardToken;
    require getRewardTokensLength() == 1;
    require getRewardToken(0) == _DummyERC20_rewardToken;
    
    //require isRegisteredRewardToken(reward); //todo: review the assumption
 
    mathint claimableRewardsBefore = getClaimableRewards(e, user, reward);
    f(e, args); 
    mathint claimableRewardsAfter = getClaimableRewards(e, user, reward);
    assert claimableRewardsAfter == claimableRewardsBefore;
}

//timeout
//should fail
rule getClaimableRewards_stable_SANITY(method f)
    filtered { f -> //claimFunctions(f)
                    f.selector == claimRewardsOnBehalf(address, address,address[]).selector   
    }
{
    env e;
    calldataarg args;
    address user;
    address reward;
    
    require user != 0;

    setup(e, user);    
    //assume a single reward
    require reward == _DummyERC20_rewardToken;
    require getRewardTokensLength() == 1;
    require getRewardToken(0) == _DummyERC20_rewardToken;
    
    //require isRegisteredRewardToken(reward); //todo: review the assumption
 
    mathint claimableRewardsBefore = getClaimableRewards(e, user, reward);
    f(e, args); 
    mathint claimableRewardsAfter = getClaimableRewards(e, user, reward);
    assert claimableRewardsAfter == claimableRewardsBefore;
}



//pass
/// @title getClaimableRewards() is stable unless rewards were claimed
/// @dev case splitting
rule getClaimableRewards_stable_after_deposit()
{
    env e;
    address user;
    address reward;
    
    uint256 assets;
    address recipient;
    uint16 referralCode;
    bool fromUnderlying = true;

    require user != 0;

    require getRewardTokensLength() == 1;

    require _RewardsController.getAvailableRewardsCount(_AToken)  > 0;
    require _RewardsController.getRewardsByAsset(_AToken, 0) == _DummyERC20_rewardToken;

    require currentContract != user;
    require _AToken != user;
    require _RewardsController !=  user;
    require _DummyERC20_aTokenUnderlying  != user;
    require _DummyERC20_rewardToken != user;
    require _SymbolicLendingPoolL1 != user;
    require _TransferStrategy != user;
    require _ScaledBalanceToken != user;
    require _TransferStrategy != user;

    //assume a single reward
    require reward == _DummyERC20_rewardToken;
    require getRewardTokensLength() == 1;
    require getRewardToken(0) == _DummyERC20_rewardToken;
    
    //require isRegisteredRewardToken(reward); //todo: review the assumption
 
    mathint claimableRewardsBefore = getClaimableRewards(e, user, reward);
    deposit(e, assets, recipient,referralCode,fromUnderlying);
    mathint claimableRewardsAfter = getClaimableRewards(e, user, reward);
    assert claimableRewardsAfter == claimableRewardsBefore;
}


// timeout
//todo: remove
/// @title getClaimableRewards() is stable unless rewards were claimed
/// @dev case splitting
rule getClaimableRewards_stable_after_atoken_transferFrom()
{
    env e;
    calldataarg args;
    address user;
    address reward;

    address sender;
    uint256 amount;
    
    require user != 0;
    mathint claimableRewardsBefore = getClaimableRewards(e, user, reward);
    _AToken.transferFrom(e, sender, currentContract, amount);
    mathint claimableRewardsAfter = getClaimableRewards(e, user, reward);
    assert claimableRewardsAfter == claimableRewardsBefore;
}


// timeout
//todo: remove
/// @title getClaimableRewards() is stable unless rewards were claimed
/// @dev case splitting, call setup()
rule getClaimableRewards_stable_after_atoken_transferFrom_1()
{
    env e;
    calldataarg args;
    address user;
    address reward;

    address sender;
    uint256 amount;
   // require isRegisteredRewardToken(reward); //todo: review the assumption
    require user != 0;
    setup(e, user);

    mathint claimableRewardsBefore = getClaimableRewards(e, user, reward);
    _AToken.transferFrom(e, sender, currentContract, amount);
    mathint claimableRewardsAfter = getClaimableRewards(e, user, reward);
    assert claimableRewardsAfter == claimableRewardsBefore;
}
 
/// @title special case of rule getClaimableRewards_stable for initialize
//fail
//todo: consider removing this rule. no method is called before initialize()
/// @title getClaimableRewards() is stable after initialize()
/// @dev case splitting
rule getClaimableRewards_stable_after_initialize(method f)
    filtered { f -> !f.isView && !claimFunctions(f) }{

    env e;
    address newAToken;
    string staticATokenName;
    string staticATokenSymbol;

    calldataarg args;
    address user;
    address reward;
    
  
    mathint claimableRewardsBefore = getClaimableRewards(e, user, reward);
    require isRegisteredRewardToken(reward); //todo: review assumption
 

    initialize(e, newAToken, staticATokenName, staticATokenSymbol);
    //assume a single reward
    //todo: allow multiple rewards
    require reward == _DummyERC20_rewardToken;
    require newAToken == _AToken;
    require getRewardTokensLength() == 1;
    require getRewardToken(0) == _DummyERC20_rewardToken;
    setup(e, user);    
    mathint claimableRewardsAfter = getClaimableRewards(e, user, reward);
    assert claimableRewardsAfter == claimableRewardsBefore;
}
//todo: remove
//pass
/// @title getClaimableRewards() is stable unless rewards were claimed
/// @dev case splitting, call setup()
rule getClaimableRewards_stable_after_refreshRewardTokens()
{

    env e;
    address user;
    address reward;
    //require isRegisteredRewardToken(reward); //todo: review assumption

    mathint claimableRewardsBefore = getClaimableRewards(e, user, reward);
    refreshRewardTokens(e);

    setup(e, user);    

    mathint claimableRewardsAfter = getClaimableRewards(e, user, reward);
    assert claimableRewardsAfter == claimableRewardsBefore;
}


/// @title The amount of rewards that was actually received by claimRewards() cannot exceed the initial amount of rewards
rule getClaimableRewardsBefore_leq_claimed_claimRewardsOnBehalf(method f)
{   
    env e;
    address onBehalfOf;
    address receiver; 
    address my_reward;
    address[] rewards;
    //setup(e, onBehalfOf, receiver);   
    
    mathint balanceBefore = _DummyERC20_rewardToken.balanceOf(onBehalfOf);
    mathint claimableRewardsBefore = getClaimableRewards(e, onBehalfOf, my_reward);
    claimRewardsOnBehalf(e, onBehalfOf, receiver, rewards);
    mathint balanceAfter = _DummyERC20_rewardToken.balanceOf(onBehalfOf);
    mathint deltaBalance = balanceAfter - balanceBefore;
   
    assert deltaBalance <= claimableRewardsBefore;
}



//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

rule sanity(method f)
{
	env e;
	calldataarg args;
	f(e,args);
	assert false;
}


//
// Examples for development
//keep these rules until a Jira ticket is opened
//

rule sanity_metaDeposit    ()
{
	env e;
	calldataarg args;
	metaDeposit(e,args);
	assert false;
}
rule sanity_metaWithdraw()
{
	env e;
	calldataarg args;
	metaWithdraw(e,args);
	assert false;
}

rule getClaimableRewards_stable_after_metaWithdraw(){

    env e;
    calldataarg args;
    address user;
    address reward;

    mathint claimableRewardsBefore = getClaimableRewards(e, user, reward);
    metaWithdraw(e, args);
    mathint claimableRewardsAfter = getClaimableRewards(e, user, reward);
    assert claimableRewardsAfter == claimableRewardsBefore;

}

rule getClaimableRewards_stable_after_withdraw(){

    env e;
    calldataarg args;
    address user;
    address reward;

    mathint claimableRewardsBefore = getClaimableRewards(e, user, reward);
    withdraw(e, args);
    mathint claimableRewardsAfter = getClaimableRewards(e, user, reward);
    assert claimableRewardsAfter == claimableRewardsBefore;

}


//     require totalSupply() <= _AToken.scaledTotalSupply();
//     require totalSupply() <= _AToken.totalSupply();
//     mathint oldInd;
//     mathint newInd;
//     oldInd, newInd = _RewardsController.getAssetIndex(e, _AToken, _DummyERC20_rewardToken);
//     require oldInd >= 1;

//     mathint oldIndRewCtrl;
//     mathint newIndRewCtrl;
//     oldIndRewCtrl, newIndRewCtrl = _RewardsController.getAssetIndex(e, _AToken, _RewardsController);
//     require oldIndRewCtrl >= 1;



// rule getClaimableRewards_after_claimRewardsToSelf()
// {
//     env e;
//     claimRewardsToSelf(e);
//     mathint claimableRewardsAfter = getClaimableRewards(e, e.msg.sender);
//     assert claimableRewardsAfter == 0;
// }

