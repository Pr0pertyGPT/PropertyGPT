using PORaggregatorDummy as aggregator

methods {
    getAssets() returns (address[]) envfree 
    enableAssets(address[])
    disableAssets(address[])
    areAllReservesBacked() returns (bool) envfree
    executeEmergencyAction() envfree
    isEmergencyActionPossible() returns (bool) envfree

    // Harness:
    enableAsset(address)
    disableAsset(address)
    getAssetState(address) returns (bool) envfree
    getAssetsLength() returns (uint256) envfree
    getAsset(uint256) returns (address) envfree
    _disableBorrowing() returns (bool) envfree
    _disableBorrowingCalled() returns (bool) envfree

    // Dummy aggregator functions:
    aggregator.areReservesBackedFlag() returns (bool) envfree
    aggregator.initFlags(bool) envfree
}

function assetsRequirements() {
    requireInvariant uniqueArray();
    requireInvariant flagConsistancy();
    require getAssetsLength() < max_uint160 - 1;
}

definition tempOmittedFunc(method f) returns bool = f.selector == executeEmergencyAction().selector;

/*
    @Rule
    @Description: The integrity of disabling an asset.
                  after calling to disableAsset(asset) the asset's state should be disabled (False).
                  If the asset already exists, then one asset should be removed,
                  otherwise, no asset should be removed.
         
    @Formula: 
        {
            assetStateBefore := getAssetState(asset),
            assetsLengthBefore := getAssetsLength()
        }
        disableAsset(asset)
        {
            !assetStateAfter,
            !assetStateAfter => assetsLengthBefore == assetsLengthAfter,
            assetStateAfter => assetsLengthBefore == assetsLengthAfter + 1
        }

    @Notes:
    @Link:
*/
rule integrityOfDisableAssets(address asset) {
    env e;
    assetsRequirements(); 
    bool assetStateBefore = getAssetState(asset);
    uint256 assetsLengthBefore = getAssetsLength();
    require assetsLengthBefore < max_uint256 - 2;
    
    disableAsset(e, asset);

    bool assetStateAfter = getAssetState(asset);
    uint256 assetsLengthAfter = getAssetsLength();

    assert !assetStateAfter;
    assert !assetStateBefore => assetsLengthBefore == assetsLengthAfter;
    assert assetStateBefore => assetsLengthBefore == assetsLengthAfter + 1;
}

/*
    @Rule
    @Description: The integrity of enabling an asset.
                  after calling to enableAsset(asset) the asset's state should be enabled.
                  If the asset already exists and enabled, then no assets should be added,
                  otherwise, one asset should be added.
    @Formula: 
        {
            assetStateBefore := getAssetState(asset),
            assetsLengthBefore := getAssetsLength()
        }
        enableAsset(asset)
        {
            assetStateAfter,
            assetStateBefore => assetsLengthBefore == assetsLengthAfter,
            !assetStateBefore => assetsLengthBefore == assetsLengthAfter - 1
        }

    @Notes:
    @Link:
*/
rule integrityOfEnableAssets(address asset) {
    env e;
    assetsRequirements();
    bool assetStateBefore = getAssetState(asset);
    uint256 assetsLengthBefore = getAssetsLength();
    require assetsLengthBefore < max_uint256 - 2;

    enableAsset(e, asset);

    bool assetStateAfter = getAssetState(asset);
    uint256 assetsLengthAfter = getAssetsLength();

    assert assetStateAfter;
    assert assetStateBefore => assetsLengthBefore == assetsLengthAfter;
    assert !assetStateBefore => assetsLengthBefore == assetsLengthAfter - 1;
}

/*
    @Rule
    @Description: enable the same asset twice is equal to enable the asset once.
         
    @Formula: 
        {
            assetStateBefore := getAssetState(asset),
            assetsLengthBefore := getAssetsLength()
        }
        enableAsset(asset)
        enableAsset(asset)
        {
            assetStateAfter2Calls := getAssetState(asset),
            assetsLengthAfter2Calls := getAssetsLength()
        }

        enableAsset(asset)
        {
            assetStateAfter1Call := getAssetState(asset),
            assetsLengthAfter1Call := getAssetsLength()
        }
        {
            assetStateAfter2Calls == assetStateAfter1Call,
            assetsLengthAfter2Calls == assetsLengthAfter1Call
        }

    @Notes:
    @Link:
*/
rule enableDuplicationsWithStorage(address asset) {
    env e;
    assetsRequirements();
    bool assetStateBefore = getAssetState(asset);
    uint256 assetsLengthBefore = getAssetsLength();
    require assetsLengthBefore < max_uint256 - 2;

    storage initialStorage = lastStorage;

    enableAsset(e, asset);
    enableAsset(e, asset);

    bool assetStateAfter2Calls = getAssetState(asset);
    uint256 assetsLengthAfter2Calls = getAssetsLength();

    enableAsset(e, asset) at initialStorage;

    bool assetStateAfter1Call = getAssetState(asset);
    uint256 assetsLengthAfter1Call = getAssetsLength();

    assert assetStateAfter2Calls == assetStateAfter1Call;
    assert assetsLengthAfter2Calls == assetsLengthAfter1Call;
}

/*
    @Rule
    @Description: disable the same asset twice is equal to disable the asset once.
         
    @Formula: 
        {
            assetStateBefore := getAssetState(asset),
            assetsLengthBefore := getAssetsLength()
        }
        disableAsset(asset)
        disableAsset(asset)
        {
            assetStateAfter2Calls := getAssetState(asset),
            assetsLengthAfter2Calls := getAssetsLength()
        }

        disableAsset(asset)
        {
            assetStateAfter1Call := getAssetState(asset),
            assetsLengthAfter1Call := getAssetsLength()
        }
        {
            assetStateAfter2Calls == assetStateAfter1Call,
            assetsLengthAfter2Calls == assetsLengthAfter1Call
        }

    @Notes:
    @Link:
*/
rule disableDuplicationsWithStorage(address asset) {
    env e;
    assetsRequirements();
    bool assetStateBefore = getAssetState(asset);
    uint256 assetsLengthBefore = getAssetsLength();
    require assetsLengthBefore < max_uint256 - 2;

    storage initialStorage = lastStorage;

    disableAsset(e, asset);
    disableAsset(e, asset);

    bool assetStateAfter2Calls = getAssetState(asset);
    uint256 assetsLengthAfter2Calls = getAssetsLength();

    disableAsset(e, asset) at initialStorage;

    bool assetStateAfter1Call = getAssetState(asset);
    uint256 assetsLengthAfter1Call = getAssetsLength();

    assert assetStateAfter2Calls == assetStateAfter1Call;
    assert assetsLengthAfter2Calls == assetsLengthAfter1Call;
}

/*
    @Rule
    @Description: call executeEmergencyAction(), if areAllReservesBacked is false then _disableborrowing() was called,
                                                else, _disableborrowing() was not called
         
    @Formula: 
        {
            allReservesBacked := areAllReservesBacked()
        }
        executeEmergencyAction()
        {
            !allReservesBacked => disableBorrowingCalled
            allReservesBacked => !disableBorrowingCalled
        }

    @Notes:
    @Link:
*/
/* !!!! Temp commented until the prover will be updated !!!! */
// rule integrityOfExecuteEmergencyAction(bool rand) {
//     require _disableBorrowingCalled() == false;
//     aggregator.initFlags(rand);
//     bool allReservesBacked = areAllReservesBacked();

//     executeEmergencyAction();

//     bool disableBorrowingCalled = _disableBorrowingCalled();

//     assert !allReservesBacked => disableBorrowingCalled;
//     assert allReservesBacked => !disableBorrowingCalled;
// }

ghost uint256 old_zero_index;
ghost mapping(address => uint256) reverseMap
{
    axiom forall address a. IS_ADDRESS(a) => IS_UINT256(reverseMap[a]);
}
ghost uint256 _assetsLength
{
    init_state axiom _assetsLength == 0;
}
ghost mapping(uint256 => address) mirrorArray;
ghost mapping(address => bool) mirrorFlag
{
    init_state axiom forall address a. IS_ADDRESS(a) => !mirrorFlag[a];
}
hook Sstore _assets.(offset 0) uint256 newLen (uint256 oldLen) STORAGE {
    require _assetsLength == oldLen;
    reverseMap[mirrorArray[to_uint256(oldLen - 1)]] = ((IS_ZERO_ADDRESS(mirrorArray[to_uint256(oldLen - 1)])) && (newLen == to_uint256(oldLen - 1))?old_zero_index:reverseMap[mirrorArray[to_uint256(oldLen - 1)]]);
    _assetsLength = newLen;
}

hook Sload uint256 len _assets.(offset 0) STORAGE {
    require _assetsLength == len;
}
hook Sstore _assets[INDEX uint256 index] address newValue (address oldValue) STORAGE {
    require mirrorArray[index] == oldValue;
    mirrorArray[index] = newValue;
    old_zero_index = (IS_ZERO_ADDRESS(newValue) && index == to_uint256(_assetsLength - 1)? reverseMap[newValue]:old_zero_index);
    reverseMap[newValue] = index;

    }
hook Sload address value _assets[INDEX uint256 index] STORAGE {
    require mirrorArray[index] == value;
}


hook Sstore _assetsState[KEY address a] bool newValue (bool oldValue) STORAGE {
    require mirrorFlag[a] == oldValue;
    mirrorFlag[a] = newValue;
    }
hook Sload bool value _assetsState[KEY address a] STORAGE {
    require mirrorFlag[a] == value;
}

definition IS_UINT256(uint256 x) returns bool = ((x >= 0) && (x <= max_uint256));
definition IS_ADDRESS(address x) returns bool = ((x >= 0) && (x <= max_uint160));
definition IS_ZERO_ADDRESS(address x) returns bool = x == 0;

/* !!!! Temp filtering until the prover will be updated !!!! */
invariant flagConsistancy()
    (forall address a. IS_ADDRESS(a) => ((mirrorFlag[a] => (((reverseMap[a] < _assetsLength) && (mirrorArray[reverseMap[a]] == a)))))) && (forall uint256 i. IS_UINT256(i) => (i < _assetsLength => (mirrorFlag[mirrorArray[i]])))
    filtered { f -> !tempOmittedFunc(f) }
    {
        preserved{
            requireInvariant uniqueArray();
            require getAssetsLength() < max_uint160 - 1;
        }
    }

/* !!!! Temp filtering until the prover will be updated !!!! */
invariant uniqueArray()
    forall uint256 i. IS_UINT256(i) => (forall uint256 j. IS_UINT256(j) => ((i < _assetsLength && j < _assetsLength) => ( i != j => mirrorArray[i] != mirrorArray[j])))
    filtered { f -> !tempOmittedFunc(f) }
    {
        preserved{
            requireInvariant flagConsistancy();
        }
    }