import "erc20.spec"


using DummyERC20_rewardToken as aRewardToken
using RewardsControllerHarness as aRewardsController


methods
{
    /*******************
    *     envfree      *
    ********************/
	getUnclaimedRewards(address user) returns (uint256) envfree
	rewardToken() returns address envfree
	aRewardToken.balanceOf(address user) returns (uint256) envfree
	incentivesController() returns (address) envfree

    /*******************
    *     Pool.sol     *
    ********************/
    // can we assume a fixed index? 1 ray?
    // getReserveNormalizedIncome(address) returns (uint256) => DISPATCHER(true)

    //in RewardsDistributor.sol called by RewardsController.sol
    getAssetIndex(address, address) returns (uint256, uint256) =>  DISPATCHER(true)
    //deposit(address,uint256,address,uint16) => DISPATCHER(true)
    //withdraw(address,uint256,address) returns (uint256) => DISPATCHER(true)
    finalizeTransfer(address, address, address, uint256, uint256, uint256) => NONDET  

    //in ScaledBalanceTokenBase.sol called by getAssetIndex
    scaledTotalSupply() returns (uint256)  => DISPATCHER(true) 
    
    //IAToken.sol
    mint(address,address,uint256,uint256) returns (bool) => DISPATCHER(true)
    burn(address,address,uint256,uint256) returns (bool) => DISPATCHER(true)

    /*******************************
    *     RewardsController.sol    *
    ********************************/
   // claimRewards(address[],uint256,address,address) => NONDET
     
   /*****************************
    *     OZ ERC20Permit.sol     *
    ******************************/
    permit(address,address,uint256,uint256,uint8,bytes32,bytes32) => NONDET

    /*********************
    *     AToken.sol     *
    **********************/
    getIncentivesController() returns (address) => CONSTANT
    UNDERLYING_ASSET_ADDRESS() returns (address) => CONSTANT
    
    /**********************************
    *     RewardsDistributor.sol     *
    **********************************/
    getRewardsList() returns (address[]) => NONDET

    /**********************************
    *     RewardsController.sol     *
    **********************************/
    //call by RewardsController.IncentivizedERC20.sol and also by StaticATokenLM.sol
    handleAction(address,uint256,uint256) => DISPATCHER(true)

    // called by  StaticATokenLM.claimRewardsToSelf  -->  RewardsController._getUserAssetBalances
    // get balanceOf and totalSupply of _aToken
    // todo - link to the actual token.
    getScaledUserBalanceAndSupply(address) returns (uint256, uint256) => DISPATCHER(true)

    // called by StaticATokenLM.collectAndUpdateRewards --> RewardsController._transferRewards()
    //implemented as simple transfer() in TransferStrategyHarness
    performTransfer(address,address,uint256) returns (bool) =>  DISPATCHER(true)

 }


// Ensures rewards are updated correctly after claiming, when there are enough
// reward funds.
/* Verified in:
https://vaas-stg.certora.com/output/98279/274946aa85a247149c025df228c71bc1?anonymousKey=5adb195fd1c025db104868af9aead15244995b7f
 */
rule rewardsConsistencyWhenSufficientRewardsExist() {
	require aRewardToken == rewardToken();

	env e;
	require e.msg.sender != currentContract;  // Cannot claim to contract
	uint256 rewardsBalancePre = aRewardToken.balanceOf(e.msg.sender);
	uint256 claimablePre = getClaimableRewards(e, e.msg.sender);

	// Ensure contract has sufficient rewards
	require aRewardToken.balanceOf(currentContract) == claimablePre;

	claimRewardsToSelf(e);

	uint256 rewardsBalancePost = aRewardToken.balanceOf(e.msg.sender);
	uint256 unclaimedPost = getUnclaimedRewards(e.msg.sender);
	uint256 claimablePost = getClaimableRewards(e, e.msg.sender);
	
	assert rewardsBalancePost >= rewardsBalancePre, "Rewards balance reduced after claim";
	uint256 rewardsGiven = rewardsBalancePost - rewardsBalancePre;
	assert claimablePre == rewardsGiven + unclaimedPost, "Rewards given unequal to claimable";
	assert claimablePost == unclaimedPost, "Claimable different from unclaimed";
}


// Ensures rewards are updated correctly after claiming, when there aren't
// enough funds.
/* Fails in:
https://vaas-stg.certora.com/output/98279/274946aa85a247149c025df228c71bc1?anonymousKey=5adb195fd1c025db104868af9aead15244995b7f
 * Probably because getUnclaimedRewards uses rayToWadRoundDown (StaticATokenLM.sol:332).
 */
rule rewardsConsistencyWhenInsufficientRewards() {
	require aRewardToken == rewardToken();

	env e;
	require e.msg.sender != currentContract;  // Cannot claim to contract
	uint256 rewardsBalancePre = aRewardToken.balanceOf(e.msg.sender);
	uint256 claimablePre = getClaimableRewards(e, e.msg.sender);

	// Ensure contract does not have sufficient rewards
	require aRewardToken.balanceOf(currentContract) < claimablePre;

	claimRewardsToSelf(e);

	uint256 rewardsBalancePost = aRewardToken.balanceOf(e.msg.sender);
	uint256 unclaimedPost = getUnclaimedRewards(e.msg.sender);
	uint256 claimablePost = getClaimableRewards(e, e.msg.sender);
	
	assert rewardsBalancePost >= rewardsBalancePre, "Rewards balance reduced after claim";
	uint256 rewardsGiven = rewardsBalancePost - rewardsBalancePre;
	if (rewardsGiven > 0) {
		assert claimablePre == rewardsGiven + unclaimedPost, "Rewards given unequal to claimable";
	} else {
		// In this case the unclaimed rewards are not updated
		assert claimablePre == claimablePost, "Claimable rewards mismatch";
	}
}

// Failed (e.g. withdraw):
// https://prover.certora.com/output/98279/ec85c3f994b84dfc9d99588955d536e7?anonymousKey=d052f9545f9a42e667a9d0965763f4967df5b790
rule rewardsTotalDeclinesOnlyByClaim(method f) {
	require aRewardsController == incentivesController();

	env e;
	require e.msg.sender != currentContract;
	require f.selector != initialize(address, address, string, string).selector;

	uint256 preTotal = getTotalClaimableRewards(e);
	uint256 preRewards = aRewardsController.getUserAccruedRewards(e, currentContract, aRewardToken);

	calldataarg args;
	f(e, args);

	uint256 postTotal = getTotalClaimableRewards(e);
	uint256 postRewards = aRewardsController.getUserAccruedRewards(e, currentContract, aRewardToken);
	require preRewards == postRewards;

	assert (postTotal < preTotal) => (
		(f.selector == claimRewardsOnBehalf(address, address).selector) ||
		(f.selector == claimRewards(address).selector) ||
		(f.selector == claimRewardsToSelf().selector)
	), "Total rewards decline not due to claim";
}


// Failed:
// https://prover.certora.com/output/98279/ca9c016adf2c4e23bc5747986621160f?anonymousKey=571190f7fa87d03513351adc13ec7eddcba0ae5c
rule rewardsTotalDoesNotDeclineByWithdraw() {
	require aRewardsController == incentivesController();

	env e;
	require e.msg.sender != currentContract;

	uint256 preTotal = getTotalClaimableRewards(e);

	calldataarg args;
	withdraw(e, args);

	uint256 postTotal = getTotalClaimableRewards(e);

	assert (postTotal >= preTotal), "Total rewards declines by withdraw";
}


rule rewardsTotalDoesNotDeclineByDeposit(uint256 assets) {
	require aRewardsController == incentivesController();

	env e;
	require e.msg.sender != currentContract;

	uint256 preTotal = getTotalClaimableRewards(e);

	deposit(e, assets, e.msg.sender);

	uint256 postTotal = getTotalClaimableRewards(e);

	assert (postTotal >= preTotal), "Total rewards declines by deposit";
}
