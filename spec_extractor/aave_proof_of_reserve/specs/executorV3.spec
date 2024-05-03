using PORaggregatorDummy as aggregator
using configuratorDummy as configurator

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

    // Dummy aggregator functions:
    aggregator.areReservesBackedFlag() returns (bool) envfree
    aggregator.initFlags(bool) envfree

    // Dummy configurator functions:
    configurator._ltv() returns (uint256) envfree
    configurator.freezeWasCalled() returns (bool) envfree
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
        enableAsset(asset)
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
    require OneToOne_arrOfTokens && (setLength == 0);
    require Consistant_flag && setLengthFlag == 0;  
    require assetInitLength == getAssetsLength();  
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
    require OneToOne_arrOfTokens && (setLength == 0);
    require Consistant_flag && setLengthFlag == 0;
    require assetInitLength == getAssetsLength();
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
    require e.msg.value == 0;
    require OneToOne_arrOfTokens && (setLength == 0);
    require Consistant_flag && setLengthFlag == 0;
    require assetInitLength == getAssetsLength();
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
    require e.msg.value == 0;
    require OneToOne_arrOfTokens && (setLength == 0);
    require Consistant_flag && setLengthFlag == 0;
    require assetInitLength == getAssetsLength();
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
    @Description: call executeEmergencyAction(), if areAllReservesBacked is false then setReserveFreeze was called,
                                                else, setReserveFreeze was not called
         
    @Formula: 
        {
            allReservesBacked := areAllReservesBacked()
        }
        executeEmergencyAction()
        {
            !allReservesBacked => setReserveFreezeWasCalled
            allReservesBacked => !setReserveFreezeWasCalled
        }

    @Notes:
    @Link:
*/
/* !!!! Temp commented until the prover will be updated !!!! */
// rule integrityOfExecuteEmergencyAction(bool rand) {
//     aggregator.initFlags(rand);
//     require configurator.freezeWasCalled() == false;
//     bool allReservesBacked = areAllReservesBacked();

//     executeEmergencyAction();

//     bool freezeReserveWasCalled = configurator.freezeWasCalled();

//     assert !allReservesBacked => freezeReserveWasCalled;
//     assert allReservesBacked => !freezeReserveWasCalled;
// }

// invariant - if asset is active then it is in _assets array

ghost mapping(uint256 => address) indexSetArrayFlag;
ghost mapping(address => uint256) indexSetShortcutFlag;
ghost mapping(address => bool) mirrorInitFlag;
ghost uint256 setLengthFlag;
ghost bool Consistant_flag;

ghost mapping(uint256 => uint256) indexSetArray;
ghost mapping(uint256 => uint256) indexSetShortcut;
ghost mapping(address => uint256) reverseMapInit;
ghost uint256 setLength;
ghost bool OneToOne_arrOfTokens;

ghost mapping(uint256 => address) mirrorInitArray;
ghost mapping(address => uint256) reverseMap;
ghost uint256 assetInitLength;

hook Sstore _assets[INDEX uint256 index] address newValue (address oldValue) STORAGE {

    // this is for the require that the _assets array is unique 
    uint256 shortcutIndex = indexSetShortcut[index];
    bool firstAccess = (shortcutIndex >= setLength) || indexSetArray[shortcutIndex] != index;
    indexSetShortcut[index] = firstAccess?setLength:indexSetShortcut[index];
    indexSetArray[setLength] = index;
    setLength = setLength + (firstAccess?to_uint256(1):to_uint256(0));
    require (OneToOne_arrOfTokens && firstAccess) => (reverseMapInit[oldValue] == index);
    //end

    require (Consistant_flag && firstAccess) => (mirrorInitFlag[oldValue]);
    require firstAccess => mirrorInitArray[index] == oldValue;
    reverseMap[newValue] = index;
    }
hook Sload address value _assets[INDEX uint256 index] STORAGE {

    //this is for the require that the _assets array is unique 
    uint256 shortcutIndex = indexSetShortcut[index];
    bool firstAccess = (shortcutIndex >= setLength) || indexSetArray[shortcutIndex] != index;
    indexSetShortcut[index] = firstAccess?setLength:indexSetShortcut[index];
    indexSetArray[setLength] = index;
    setLength = setLength + (firstAccess?to_uint256(1):to_uint256(0));
    require (OneToOne_arrOfTokens && firstAccess) => (reverseMapInit[value] == index);
    //end

    require (Consistant_flag && firstAccess) => (mirrorInitFlag[value]);
    require firstAccess => mirrorInitArray[index] == value;
}


hook Sstore _assetsState[KEY address a] bool newValue (bool oldValue) STORAGE {

    //this is for the require that the validator array is unique 
    uint256 shortcutIndex = indexSetShortcutFlag[a];
    bool firstAccess = (shortcutIndex >= setLengthFlag) || indexSetArrayFlag[shortcutIndex] != a;
    indexSetShortcutFlag[a] = firstAccess?setLengthFlag:indexSetShortcutFlag[a];
    indexSetArrayFlag[setLengthFlag] = a;
    setLengthFlag = setLengthFlag + (firstAccess?to_uint256(1):to_uint256(0));
    require firstAccess => (mirrorInitFlag[a] == oldValue);
    require (Consistant_flag && firstAccess && oldValue) => (reverseMapInit[a] < assetInitLength);
    require (Consistant_flag && firstAccess && oldValue) => mirrorInitArray[reverseMapInit[a]] == a;
    //end

    }
hook Sload bool value _assetsState[KEY address a] STORAGE {

    //this is for the require that the validator array is unique 
    uint256 shortcutIndex = indexSetShortcutFlag[a];
    bool firstAccess = (shortcutIndex >= setLengthFlag) || indexSetArrayFlag[shortcutIndex] != a;
    indexSetShortcutFlag[a] = firstAccess?setLengthFlag:indexSetShortcutFlag[a];
    indexSetArrayFlag[setLengthFlag] = a;
    setLengthFlag = setLengthFlag + (firstAccess?to_uint256(1):to_uint256(0));
    require firstAccess => (mirrorInitFlag[a] == value);
    require (Consistant_flag && firstAccess && value) => (reverseMapInit[a] < assetInitLength);
    require (Consistant_flag && firstAccess && value) => mirrorInitArray[reverseMapInit[a]] == a;
    //end
}

/* !!!! Temp filtering until the prover will be updated !!!! */
invariant flagConsistancy(uint256 i)
    i < getAssetsLength() => getAssetState(getAsset(i))
    filtered { f -> !tempOmittedFunc(f) }
    {
        preserved{
            require OneToOne_arrOfTokens && (setLength == 0);
            require Consistant_flag && setLengthFlag == 0;
        }
    }

/* !!!! Temp filtering until the prover will be updated !!!! */
invariant flagConsistancy2(address val)
    getAssetState(val) => getAsset(reverseMap[val]) == val || val == 0
    filtered { f -> !tempOmittedFunc(f) }
    {
        preserved{
            require OneToOne_arrOfTokens && (setLength == 0);
            require Consistant_flag && setLengthFlag == 0;
            require getAssetsLength() < max_uint256 - 10;
        }
    }

/* !!!! Temp filtering until the prover will be updated !!!! */
invariant uniqueArray(uint256 i, uint256 j)
    i != j => ((getAsset(i) != getAsset(j)) || (i >= getAssetsLength() ||  j >= getAssetsLength()))
    filtered { f -> !tempOmittedFunc(f) }
    {
        preserved{
            require OneToOne_arrOfTokens && (setLength == 0);
            require Consistant_flag && setLengthFlag == 0;
        }
    }
