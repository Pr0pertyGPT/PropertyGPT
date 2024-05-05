////////////////////////////////////////////////////////////////////////////
//                       Imports and multi-contracts                      //
////////////////////////////////////////////////////////////////////////////
import "./setup.spec"

use invariant alwaysUnSent // Imports the invariant alwaysUnSent
use invariant ATokenAssetPair // Imports the invariant ATokenAssetPair

////////////////////////////////////////////////////////////////////////////
//                       Rules                                            //
////////////////////////////////////////////////////////////////////////////

// Checks basic properties of withdrawal:
// 1. Rreward token balance cannot be decreased
// 2. Depending on what token was chosen to be withdrawed, the AToken/undelying token's balance mustn't decrease, while the other doesnt change
rule integrityOfWithdraw(address recipient){
    bool toUnderlyingAsset;
    uint256 staticAmount; 
    env e; calldataarg args;
    address underlying;
    address static;
    address aToken;
    uint256 l2RewardsIndex = BRIDGE_L2.l2RewardsIndex();
    
    setupTokens(underlying, aToken, static);
    setupUser(e.msg.sender);
    require recipient != aToken;
    require recipient != currentContract;

    uint256 underlyingBalanceBefore = tokenBalanceOf(e, underlying, recipient);
    uint256 aTokenBalanceBefore = tokenBalanceOf(e, aToken, recipient);
    uint256 rewardTokenBalanceBefore = tokenBalanceOf(e, REWARD_TOKEN, recipient);

    initiateWithdraw_L2(e, aToken, staticAmount, recipient, toUnderlyingAsset);

    uint256 underlyingBalanceAfter = tokenBalanceOf(e, underlying, recipient);
    uint256 aTokenBalanceAfter = tokenBalanceOf(e, aToken, recipient);
    uint256 rewardTokenBalanceAfter = tokenBalanceOf(e, REWARD_TOKEN, recipient);

    if (toUnderlyingAsset){
        assert 
        (underlyingBalanceAfter >= underlyingBalanceBefore) &&
        (aTokenBalanceAfter == aTokenBalanceBefore);
    }
    else {
        assert 
        (aTokenBalanceAfter >= aTokenBalanceBefore) &&
        (underlyingBalanceAfter == underlyingBalanceBefore);

    }
    assert rewardTokenBalanceAfter >= rewardTokenBalanceBefore;
}


// If a balance of tokens changed, then deposit or withdrawal must have been called.
rule balanceOfUnderlyingAssetChanged(method f, uint256 amount)
filtered{f -> messageSentFilter(f) && !f.isView} {
    env e;    
    address asset;
    address AToken;
    address static;
    address recipient;
    bool fromToUA;
    
    setupTokens(asset, AToken, static);
    setupUser(e.msg.sender);

    // Underlying asset balances of sender and recipient before call.
    uint256 recipientBalanceA1 = tokenBalanceOf(e, AToken, recipient);
    uint256 recipientBalanceU1 = tokenBalanceOf(e, asset, recipient);

    // Call any interface function 
    callFunctionSetParams(f, e, recipient, AToken, asset, amount, fromToUA);

    // Underlying asset balances of sender and recipient after call.
    uint256 recipientBalanceA2 = tokenBalanceOf(e, AToken, recipient);
    uint256 recipientBalanceU2 = tokenBalanceOf(e, asset, recipient);

    bool balancesChanged = !(
        recipientBalanceA1 == recipientBalanceA2 && 
        recipientBalanceU1 == recipientBalanceU2);

    assert balancesChanged =>
            (f.selector == deposit(address, uint256, uint256, uint16, bool).selector 
            ||
            f.selector == initiateWithdraw_L2(address, uint256, address, bool).selector
            ||
            f.selector == cancelDeposit(address,uint256,uint256,uint256,uint256,uint256).selector)
            , "balanceOf changed";
}


// A call to deposit and a subsequent call to withdraw with the same amount of 
// staticATokens received, should yield the same original balance for the user.
// For underlying tokens, the condition is modified by a bound, since staticToDynamic is not inversible with dyanmicToStatic.
rule depositWithdrawReversed(uint256 amount)
{
    env eB; env eF;
    address Atoken; // AAVE Token
    address asset;  // underlying asset
    address static; // staticAToken
    uint256 l2Recipient = BRIDGE_L2.address2uint256(eF.msg.sender);
    uint16 referralCode;
    bool fromUA; // (deposit) from underlying asset
    bool toUA; // (withdraw) to underlying asset

    setupTokens(asset, Atoken, static);
    setupUser(eB.msg.sender);
    uint256 indexL1 = LENDINGPOOL_L1.liquidityIndexByAsset(asset);
    require indexL1 >= RAY() && indexL1 <= 2*RAY();

    uint256 balanceU1 = tokenBalanceOf(eB, asset, eB.msg.sender);
    uint256 balanceA1 = tokenBalanceOf(eB, Atoken, eB.msg.sender);
    uint256 balanceS1 = tokenBalanceOf(eB, static, eB.msg.sender);
        uint256 staticAmount = deposit(eB, Atoken, l2Recipient, amount, referralCode, fromUA);
    /////////////////////////
    /*
    One can use these values (post-deposit pre-withdrawal) for debugging.
    uint256 balanceU2 = tokenBalanceOf(eB, asset, eB.msg.sender);
    uint256 balanceA2 = tokenBalanceOf(eB, Atoken, eB.msg.sender);
    uint256 balanceS2 = tokenBalanceOf(eB, static, eB.msg.sender);
    */
    /////////////////////////
        initiateWithdraw_L2(eF, Atoken, staticAmount, eB.msg.sender, toUA);
    uint256 balanceU3 = tokenBalanceOf(eF, asset, eB.msg.sender);
    uint256 balanceA3 = tokenBalanceOf(eF, Atoken, eB.msg.sender);
    uint256 balanceS3 = tokenBalanceOf(eF, static, eB.msg.sender);
    
    assert balanceS1 == balanceS3;
    assert fromUA == toUA => balanceU3 - balanceU1 <= (indexL1/RAY()+1)/2;
    assert fromUA == toUA => balanceA3 == balanceA1;
}


// Checks that the transitions between static to dynamic are inverses.
rule dynamicToStaticInversible1(uint256 amount)
{
    // We assume both indexes (L1,L2) are represented in Ray (1e27).
    address asset;
    requireRayIndex(asset);
    uint256 dynm = _staticToDynamicAmount_Wrapper(amount, asset, LENDINGPOOL_L1);
    uint256 stat = _dynamicToStaticAmount_Wrapper(dynm, asset, LENDINGPOOL_L1);
    assert amount == stat;
}


// 2 rules that Checks it isn't possible to gain from transforming dynamic to static
// and back.
// *** This is violated because the mul and div are not inverses of each other,
// therefore can lead to mul(div(a,b),b) > a (depends on remainder value).
rule dynamicToStaticInversible2(uint256 amount)
{
    // We assume both indexes (L1,L2) are represented in Ray (1e27).
    address asset;
    requireRayIndex(asset);
    uint256 indexL1 = LENDINGPOOL_L1.liquidityIndexByAsset(asset);
    uint256 stat = _dynamicToStaticAmount_Wrapper(amount, asset, LENDINGPOOL_L1);
    uint256 dynm = _staticToDynamicAmount_Wrapper(stat, asset, LENDINGPOOL_L1);
     assert dynm == amount;  // Violated
}

rule dynamicToStaticInversible3(uint256 amount)
{
    // We assume both indexes (L1,L2) are represented in Ray (1e27).
    address asset;
    requireRayIndex(asset);
    uint256 indexL1 = LENDINGPOOL_L1.liquidityIndexByAsset(asset);
    uint256 stat = _dynamicToStaticAmount_Wrapper(amount, asset, LENDINGPOOL_L1);
    uint256 dynm = _staticToDynamicAmount_Wrapper(stat, asset, LENDINGPOOL_L1);
    assert dynm - amount <= (indexL1/RAY() + 1)/2; // Pass
}


// Check consistency of 'asset' being registered as the underlying
// token of 'AToken', both in the AToken contract, and also in the 
// mapping _aTokenData.
// We exclude the 'initialize' function since it is called only once
// in the code. 
invariant underlying2ATokenConsistency(address AToken, address asset)
     (asset !=0 <=> AToken !=0) 
     =>
     (getUnderlyingAssetHelper(AToken) == asset 
     <=>
     getUnderlyingAssetOfAToken(AToken) == asset)
     filtered{f-> excludeInitialize(f) && messageSentFilter(f)}


// The aToken-asset pair should be correctly registered after calling
// initialize, right after the constructor.
// This is complementary to the two invariants above.
rule initializeIntegrity(address AToken, address asset)
{
    env e;
    calldataarg args;

    // Post-constructor conditions
    require getUnderlyingAssetHelper(AToken) == 0;
    require getATokenOfUnderlyingAsset(LENDINGPOOL_L1, asset) == 0;
    
    initialize(e, args);

    assert (asset !=0 && AToken !=0) => (
        getUnderlyingAssetHelper(AToken) == asset 
        <=>
        getATokenOfUnderlyingAsset(LENDINGPOOL_L1, asset) == AToken);
}


rule cancelAfterDepositGivesBackExactAmount(uint256 amount) {
    
    env e1;
    env e2;
    env e3;
    address user = e1.msg.sender;
    address asset ;
    address aToken;
    address static ;
    address recipient;
    bool fromUA;
    uint256 rewardsIndex;
    uint256 blockNumber;
    uint256 nonce;
    uint16 code;

    setupTokens(asset, aToken, static);
    requireValidUser(user);
    requireRayIndex(asset);
    require e1.msg.sender == e2.msg.sender;
    require e2.msg.sender == e3.msg.sender;
    require e1.block.timestamp <= e2.block.timestamp;
    require e2.block.timestamp < e3.block.timestamp;

    uint256 ATokenBalance1 = tokenBalanceOf(e1, aToken, user);
    uint256 assetBalance1 = tokenBalanceOf(e1, asset, user);
        uint256 staticAmount = deposit(e1, aToken, recipient, amount, code, fromUA);
        startDepositCancellation(e2, aToken, staticAmount, recipient, rewardsIndex, blockNumber, nonce);
        cancelDeposit(e3, aToken, staticAmount, recipient, rewardsIndex, blockNumber, nonce);
    uint256 ATokenBalance2 = tokenBalanceOf(e3, aToken, user);
    uint256 assetBalance2 = tokenBalanceOf(e3, asset, user);

    if(fromUA){
        assert assetBalance1 == assetBalance2 + amount;
        assert ATokenBalance2 == ATokenBalance1 + amount;  
    }
    else {
        assert assetBalance1 == assetBalance2;
        assert ATokenBalance1 == ATokenBalance2;
    }
}


rule cannotCancelDepositAndGainBothTokens(address user, uint256 amount) {
    env e1; env e2; env e3;
    calldataarg args1;
    address asset;
    address aToken;
    address static;
    uint256 recipient = BRIDGE_L2.address2uint256(user);
    uint16 code;
    bool fromUA;
    uint256 rewardsIndex;
    uint256 blockNumber;
    uint256 nonce;

    setupTokens(asset, aToken, static);
    setupUser(user);
    require user == e1.msg.sender;
    require user == e2.msg.sender;
    require user == e3.msg.sender;
    
    uint256 ATokenBalance1 = tokenBalanceOf(e1, aToken, user);
    uint256 staticBalance1 = tokenBalanceOf(e1, static, user);

    uint256 staticAmount = deposit(e1, aToken, recipient, amount, code, fromUA);
    
    uint256 ATokenBalance2 = tokenBalanceOf(e1, aToken, user);
    uint256 staticBalance2 = tokenBalanceOf(e1, static, user);

    startDepositCancellation(e2, aToken, staticAmount, recipient, rewardsIndex, blockNumber, nonce);
    cancelDeposit(e3, aToken, staticAmount, recipient, rewardsIndex, blockNumber, nonce);
    
    uint256 ATokenBalance3 = tokenBalanceOf(e3, aToken, user);
    uint256 staticBalance3 = tokenBalanceOf(e3, static, user);

    // If static tokens were minted, no deposit cancellation should succeed.
    assert staticBalance2 > staticBalance1 => ATokenBalance3 == ATokenBalance2;
}

/*
Cannot be verified with the given requirements.
rule afterCancellationStartMustSucceed(uint256 amount, address user) {
    env e1; env e2;
    address asset;
    address aToken;
    address static;
    setupTokens(asset, aToken, static);
    uint256 recipient = BRIDGE_L2.address2uint256(user);
    bool fromUA;
    uint256 rewardsIndex;
    uint256 blockNumber;
    uint256 nonce;

    uint256 dynamic = _staticToDynamicAmount_Wrapper(amount, asset, LENDINGPOOL_L1);
    require amount < 2^127;
    require tokenBalanceOf(e2, aToken, currentContract) >= dynamic;
    require tokenBalanceOf(e2, asset, currentContract) >= amount;
    require e1.block.timestamp > 0;
    require e2.block.timestamp > e1.block.timestamp;
    startDepositCancellation(e1, aToken, amount, recipient, rewardsIndex, blockNumber, nonce);
    cancelDeposit@withrevert(e2, aToken, amount, recipient, rewardsIndex, blockNumber, nonce);
    bool cancelReverted = lastReverted;

    assert cancelReverted <=> !readyToCancel(e2, nonce);
}
*/

////////////////////////////////////////////////////////////////////////////
//                       Community rules                                  //
////////////////////////////////////////////////////////////////////////////

// By Jonatascm:

//Total of l2TokenAddresses
ghost mathint totalApprovedTokens {
    init_state axiom totalApprovedTokens == 0;
}

// Updates the ghost when change l2TokenAddress
hook Sstore _aTokenData[KEY address token].l2TokenAddress uint256 new_tokenAddress
    (uint256 old_tokenAddress) STORAGE {
        totalApprovedTokens = totalApprovedTokens + 1;
}

// Check integrity of _approvedL1Tokens array lenght and totalApprovedTokens change
// excluding initialize
invariant integrityApprovedTokensAndTokenData()
    totalApprovedTokens == getApprovedL1TokensLength()
    filtered{f -> messageSentFilter(f) && excludeInitialize(f)}
    { preserved { 
        // Avoiding overflow
        require getApprovedL1TokensLength() < MAX_ARRAY_LENGTH(); 
    } }

// Verify if initialize check for invalid array of l1Tokens and l2Tokens.
// Issue: There isn't a check for duplicated l2Token addresses 
rule shouldRevertInitializeTokens(address AToken, address asset){
    env e;
    uint256 l2Bridge;
    address msg;
    address controller;
    address l1TokenA;
    address l1TokenB;
    uint256 l2Token;
    // Addition by Certora, to match new interface.
    uint256 ceil1;
    uint256 ceil2;

    // Post-constructor conditions
    require getUnderlyingAssetHelper(AToken) == 0;
    require getATokenOfUnderlyingAsset(LENDINGPOOL_L1, asset) == 0;
    require getL2TokenOfAToken(l1TokenA) == 0 
        && getL2TokenOfAToken(l1TokenB) == 0;

    // In this case, both l1Tokens point to same l2Token :
    // L1TokenA => L2Token
    // L1TokenB => L2Token
    initialize@withrevert(e, l2Bridge, msg, controller,
     [l1TokenA, l1TokenB], [l2Token,l2Token], [ceil1, ceil2]);
    assert lastReverted;
}

/*
By jessicapointing
@Description:
        Expands on integrityOfDeposit rule 
        If depositing from underlying asset, then:
        (1) Sender's underlying asset should decrease by amount deposited
        (2) Sender's aToken balance should remain the same
        (3) Recipient's staticAToken balance should increase by (static) amount deposited 

        If depositing from aToken, then:
        (1) Sender's underlying asset should remain the same
        (2) Sender's aToken balance should decrease by amount deposited (according to bound)
        (3) Recipient's staticAToken balance should increased by (static) amount deposited
    @Methods:
        deposit
    @Sanity:
        PASSES
    @Outcome:
        PASSES (after Cerotra fix)
*/
rule integrityOfDepositExpanded(){
    env e; 
    address recipient;
    uint256 amount;
    address aToken;
    address underlyingAsset; 
    address staticAToken;
    uint256 l2Recipient = BRIDGE_L2.address2uint256(recipient);
    uint16 referralCode;
    bool fromUnderlyingAsset; 
    uint256 indexL1 = LENDINGPOOL_L1.liquidityIndexByAsset(underlyingAsset);
    
    setupTokens(underlyingAsset, aToken, staticAToken);
    setupUser(e.msg.sender);
    setupUser(recipient);
    requireRayIndex(underlyingAsset);
    // Recipient balances before
    uint256 recipientUnderlyingAssetBalanceBefore = tokenBalanceOf(e, underlyingAsset, recipient);
    uint256 recipientATokenBalanceBefore = tokenBalanceOf(e, aToken, recipient);
    uint256 recipientStaticATokenBalanceBefore = tokenBalanceOf(e, staticAToken, recipient);
    uint256 recipientRewardTokenBalanceBefore = tokenBalanceOf(e, REWARD_TOKEN, recipient);
    // Sender balances before
    uint256 senderUnderlyingAssetBalanceBefore = tokenBalanceOf(e, underlyingAsset, e.msg.sender);
    uint256 senderATokenBalanceBefore = tokenBalanceOf(e, aToken, e.msg.sender);
    uint256 senderStaticATokenBalanceBefore = tokenBalanceOf(e, staticAToken, e.msg.sender);
    uint256 senderRewardTokenBalanceBefore = tokenBalanceOf(e, REWARD_TOKEN, e.msg.sender); 
    uint256 staticAmount = deposit(e, aToken, l2Recipient, amount, referralCode, fromUnderlyingAsset);
    // Recipient balances after
    uint256 recipientUnderlyingAssetBalanceAfter = tokenBalanceOf(e, underlyingAsset, recipient);
    uint256 recipientATokenBalanceAfter = tokenBalanceOf(e, aToken, recipient);
    uint256 recipientStaticATokenBalanceAfter = tokenBalanceOf(e, staticAToken, recipient);
    uint256 recipientRewardTokenBalanceAfter = tokenBalanceOf(e, REWARD_TOKEN, recipient);
    // Sender balances after
    uint256 senderUnderlyingAssetBalanceAfter = tokenBalanceOf(e, underlyingAsset, e.msg.sender);
    uint256 senderATokenBalanceAfter = tokenBalanceOf(e, aToken, e.msg.sender);
    uint256 senderStaticATokenBalanceAfter = tokenBalanceOf(e, staticAToken, e.msg.sender);
    uint256 senderRewardTokenBalanceAfter = tokenBalanceOf(e, REWARD_TOKEN, e.msg.sender); 
           
    if (fromUnderlyingAsset){
        assert 
        (senderUnderlyingAssetBalanceAfter == senderUnderlyingAssetBalanceBefore - amount) &&
        (senderATokenBalanceAfter == senderATokenBalanceBefore) &&
        (recipientStaticATokenBalanceAfter == recipientStaticATokenBalanceBefore + staticAmount);
    }
    else {
        assert 
        (senderUnderlyingAssetBalanceAfter == senderUnderlyingAssetBalanceBefore) &&
        (senderATokenBalanceAfter - senderATokenBalanceBefore + amount <= (indexL1/RAY() + 1)/2) &&
        (recipientStaticATokenBalanceAfter == recipientStaticATokenBalanceBefore + staticAmount);
    }
    if (e.msg.sender != recipient) {
        assert 
        (senderStaticATokenBalanceAfter == senderStaticATokenBalanceBefore) &&
        (recipientUnderlyingAssetBalanceAfter == recipientUnderlyingAssetBalanceBefore) &&
        (recipientATokenBalanceAfter == recipientATokenBalanceBefore);
    }
    assert senderRewardTokenBalanceAfter == senderRewardTokenBalanceBefore &&
           recipientRewardTokenBalanceAfter == recipientRewardTokenBalanceBefore;
}
