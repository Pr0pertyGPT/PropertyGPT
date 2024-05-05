// STATUS - in progress
rule transition_balThisZero(address user, method f, env e) {
    safeAssumptions(e);
    require currentPhase(e) == PhaseThree();

    uint256 wavaxBalanceBefore = getWAVAXbalanceOfThis();
    uint256 wavaxPairBalanceBefore = getWAVAXbalanceOfPair();
    uint256 avaxAllocBefore = avaxAllocated();

    require open();
    calldataarg args;
    createPair(e);
    require closed();

    uint256 wavaxBalanceAfter = getWAVAXbalanceOfThis();

    assert wavaxBalanceBefore == wavaxBalanceAfter, "wavax balance of LE contract was changed";
    assert getWAVAXbalanceOfPair() - wavaxPairBalanceBefore == avaxAllocated(), "correlation is wrong";
}


// STATUS - in progress
// check exists
// - if I deposit more AVAX, eventually I receive more LP and launch tokens
rule hl_moreDepositMoreGet(method f, env e, env e2, env e3, env e4, env e5){
    require e.msg.sender != e2.msg.sender;
    require e.msg.sender != e3.msg.sender;
    require e2.msg.sender != e3.msg.sender;
    require e.msg.sender != issuer();
    require e2.msg.sender != issuer();
    require e.msg.sender != currentContract;
    require e2.msg.sender != currentContract;
    require e3.msg.sender != currentContract;
    require e.msg.value > e2.msg.value;
    require e.msg.sender == e4.msg.sender;  // need two more envs because depositAVAX() is payble but pairBalance() and getIncentives() aren't thus need the same addresses but different e.msg.value == 0 and != 0
    require e2.msg.sender == e5.msg.sender;
    require !userHasWithdrawnIncentives(e.msg.sender);
    require !userHasWithdrawnIncentives(e2.msg.sender);

    require open();

    depositAVAX(e);
    depositAVAX(e2);

    createPair(e3);

    uint256 incentivesBalanceOne = getIncentives(e4, e4.msg.sender);
    uint256 incentivesBalanceTwo = getIncentives(e5, e5.msg.sender);

    uint256 pairBalanceOne = pairBalance(e4, e4.msg.sender);
    uint256 pairBalanceTwo = pairBalance(e5, e5.msg.sender);
    
    assert exists uint256 dt. e.msg.value - e2.msg.value > dt => incentivesBalanceOne > incentivesBalanceTwo;
    // assert exists uint256 dt. e.msg.value - e2.msg.value > dt => pairBalanceOne > pairBalanceTwo;
}


// STATUS - in progress
// - if I withdraw AVAX later, I eventually have a greater penalty
rule hl_withdrawLateMorePenalty(method f, env e, env e2){
    require auctionStart() < e.block.timestamp;
    require e.block.timestamp < e2.block.timestamp;
    require phaseOneNoFeeDuration() == oneDay();
    require phaseOneDuration() == twoDays();
    require e.block.timestamp > auctionStart() + phaseOneNoFeeDuration();
    require e.block.timestamp < auctionStart() + phaseOneDuration();
    require e2.block.timestamp < auctionStart() + phaseOneDuration();

    uint256 earlyPenalty = getPenalty(e);
    uint256 latePenalty = getPenalty(e2);

    assert exists uint256 dt. e2.block.timestamp - e.block.timestamp > dt => latePenalty > earlyPenalty;
}
