methods {
    getProofOfReserveFeedForAsset(address) returns (address) envfree
    disableProofOfReserveFeed(address)
    enableProofOfReserveFeed(address, address)
    areAllReservesBacked(address[]) returns (bool, bool[]) envfree
    getBridgeWrapperForAsset(address) returns (address) envfree
    enableProofOfReserveFeedWithBridgeWrapper(address, address, address)

    // summarizations:
    latestRoundData() => NONDET
    // Getters: 
    allBacked() returns (bool) envfree
}


// calling function with specific parameters
function call_f_with_params(method f, env e, address asset , address PoRFeed, address wrapper){
    calldataarg args;
    if (f.selector == enableProofOfReserveFeed(address, address).selector){
        enableProofOfReserveFeed(e, asset, PoRFeed);
    } else if (f.selector == disableProofOfReserveFeed(address).selector){
        disableProofOfReserveFeed(e, asset);
    } else if (f.selector == enableProofOfReserveFeedWithBridgeWrapper(address, address, address).selector) {
        enableProofOfReserveFeedWithBridgeWrapper(e, asset, PoRFeed, wrapper);
    } else {
        f(e, args);
    }
}

// modification to the PoR feed of assets
// if enableProofOfReserveFeed called -> price feed must be a non-zero address
// if enableProofOfReserveFeedWithBridgeWrapper called -> price feed and bridgeWrapper must be a non-zero address
// if disableProofOfReserveFeed called -> price feed and bridgeWrapper assigned to the asset must be nullified
// if any other function called -> price and bridgeWrapper mustn't change
rule PoRFeedChange(address asset, address PoRFeed, address wrapper){
    
    address feedBefore = getProofOfReserveFeedForAsset(asset);
    address bridgeWrapperBefore = getBridgeWrapperForAsset(asset);
    
    method f; env e;
    call_f_with_params(f, e, asset, PoRFeed, wrapper);

    address feedAfter = getProofOfReserveFeedForAsset(asset);
    address bridgeWrapperAfter = getBridgeWrapperForAsset(asset);

    assert f.selector == enableProofOfReserveFeed(address, address).selector => (feedAfter != 0 && feedAfter == PoRFeed);
    assert f.selector == enableProofOfReserveFeedWithBridgeWrapper(address, address, address).selector => 
                        (feedAfter != 0 && feedAfter == PoRFeed && bridgeWrapperAfter != 0 && bridgeWrapperAfter == wrapper);
    assert f.selector == disableProofOfReserveFeed(address).selector => feedAfter == 0 && bridgeWrapperAfter == 0;
    assert (f.selector != enableProofOfReserveFeed(address, address).selector && 
            f.selector != disableProofOfReserveFeed(address).selector &&
            f.selector != enableProofOfReserveFeedWithBridgeWrapper(address, address, address).selector) => 
                        feedBefore == feedAfter && bridgeWrapperBefore == bridgeWrapperAfter;
}

// if areAllReservesBacked is false then at least one slot in tokenBacked array is false, otherwise all slots in tokenBacked array is true.
rule notAllReservesBacked_UnbackedArry_Correlation(){
    env e; address[] assets;
    
    bool reservesArrayIsBacked = areAllReservesBackedCorrelation(e, assets);
    bool areAllReservesBacked = allBacked();
    assert reservesArrayIsBacked == areAllReservesBacked;
}
