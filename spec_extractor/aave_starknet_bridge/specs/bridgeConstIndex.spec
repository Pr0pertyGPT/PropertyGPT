////////////////////////////////////////////////////////////////////////////
//                       Imports and multi-contracts                      //
////////////////////////////////////////////////////////////////////////////
import "./setup.spec"

methods {
/******************
 *     Ray Math   *
 ******************/
 // See also notes at bottom of file (under "Summarizations")
 // Comment out the next two lines to remove the simplification,
 // and let the prover use the original library functions.
   rayMul(uint256 a, uint256 b) returns (uint256) => rayMulConst(a, b)
   rayDiv(uint256 a, uint256 b) returns (uint256) => rayDivConst(a, b)
}

use invariant alwaysUnSent // Imports the invariant alwaysUnSent
use invariant ATokenAssetPair // Imports the invariant ATokenAssetPair

////////////////////////////////////////////////////////////////////////////
//                       Rules                                            //
////////////////////////////////////////////////////////////////////////////

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

////////////////////////////////////////////////////////////////////////////
//                       Community rules                                  //
////////////////////////////////////////////////////////////////////////////

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
        (senderATokenBalanceBefore - senderATokenBalanceAfter - amount <= (indexL1/RAY() + 1)/2) &&
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

