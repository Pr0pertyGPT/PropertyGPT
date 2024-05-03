using Registry as registry
using DummyERC20A as someToken
using DummyERC20B as someToken2
using ProxyHarness as proxy // may also be the same as currentContract
using Summary as summaryInstance // general summary for DeFi protocols

methods {
    // Shared-storage related
    getSlot(uint slot) returns (uint) envfree
    cache(bytes32) returns (bytes32) envfree
    getSender() returns (address) envfree
    getCubeCounter() returns (uint256) envfree
    getStackLength() returns (uint256) envfree
    isHandler() returns (bool) envfree
    MSG_SENDER_KEY() returns (bytes32) envfree
    CUBE_COUNTER_KEY() returns (bytes32) envfree
    getStackLengthSlot() returns (uint256) envfree
    ethBalance(address) returns (uint256) envfree

    // registry dispatches
    handlers(address) returns (bytes32) => DISPATCHER(true)
    callers(address) returns (bytes32) => DISPATCHER(true)
    bannedAgents(address) returns (uint256) => DISPATCHER(true)
    fHalt() returns (bool) => DISPATCHER(true)
    owner() returns (address) => DISPATCHER(true)
    isValidCaller(address) returns (bool) => DISPATCHER(true)
    isValidHandler(address) returns (bool) => DISPATCHER(true)
    
    registry.bannedAgents(address) returns (uint256) envfree
    registry.fHalt() returns (bool) envfree

    // for abstracting exec of handler
    0x12345678 => NONDET

    // ERC20
    transfer(address,uint256) => DISPATCHER(true)
    transferFrom(address,address,uint256) => DISPATCHER(true)
    approve(address,uint256) => DISPATCHER(true)
    allowance(address,address) returns (uint) => DISPATCHER(true)
    balanceOf(address) returns (uint) => DISPATCHER(true)
    totalSupply() returns (uint) => DISPATCHER(true)

    havocMe(address) => DISPATCHER(true)
    havocMeEth() => DISPATCHER(true)

    ETH_ADDRESS() returns (address) => DISPATCHER(false)
    WETH() returns (address) => DISPATCHER(false)

    someToken.balanceOf(address) returns (uint) envfree
    someToken.allowance(address,address) returns (uint) envfree
    someToken2.balanceOf(address) returns (uint) envfree

    // Summary correctness
    summaryInstance.consumedToken() returns (address) envfree
    summaryInstance.generatedToken() returns (address) envfree
    summaryInstance.shouldBeConsumedAmount() returns (uint) envfree
    summaryInstance.getBalance(address,address) returns (uint) envfree
    summaryInstance.erc20A() returns (address) envfree
    summaryInstance.erc20B() returns (address) envfree
    summaryInstance.getEthAddress(address) returns (address) envfree

    // HMaker
    proxies(address) => NONDET
    gem() => NONDET
    // also HSCompound
    execute(address,bytes) returns (bytes32) => DISPATCHER(true) // should modify/havoc erc20 balances. The returns part is super important for soundness!
    freeETH(address cdpManager,address ethJoin,uint256 cdp,uint256 wad) => DISPATCHER(true)
    freeGem(address cdpManager,address gemJoin,uint256 cdp,uint256 wad) => DISPATCHER(true)
    
    // HSCompound
    claimComp(address) => DISPATCHER(true) 

    // HAaveProtocol
    getLendingPool() => NONDET
    getLendingPoolCore() => NONDET
    getReserveATokenAddress(address) => NONDET
    deposit(address,uint256,uint16) => DISPATCHER(true)
    redeem(uint256) => DISPATCHER(true)
    flashLoan(address,address,uint256,bytes) => DISPATCHER(true)
    underlyingAssetAddress() => NONDET

    // Dispatch if should link our proxy (e.g. flashloan)
    execs(address[],bytes32[],bytes[]) => DISPATCHER(true)

    // HAaveProtocol2
    borrow(address,uint256,uint256,uint16,address) => DISPATCHER(true)
    deposit(address,uint256,address,uint16) => DISPATCHER(true)
    flashLoan(address,address[],uint256[],uint256[],address,bytes,uint16) => DISPATCHER(true)
    repay(address,uint256,uint256,address) => DISPATCHER(true)
    withdraw(address,uint256,address) => DISPATCHER(true)
    getReserveData(address) => NONDET

    // WETH
    withdraw(uint256) => DISPATCHER(true)
    deposit() => DISPATCHER(true);

    // HUniswap
    // addLiquidity(uint256,uint256,uint256) => DISPATCHER(true)
    // removeLiquidity(uint256,uint256,uint256,uint256) => DISPATCHER(true)
    // ethToTokenSwapInput(uint256,uint256) => DISPATCHER(true)
    // ethToTokenSwapOutput(uint256,uint256) => DISPATCHER(true)
    // tokenToEthSwapInput(uint256,uint256,uint256) => DISPATCHER(true)
    // tokenToEthSwapOutput(uint256,uint256,uint256) => DISPATCHER(true)
    // tokenToTokenSwapInput(uint256,uint256,uint256,uint256,address) => DISPATCHER(true)
    // tokenToTokenSwapOutput(uint256,uint256,uint256,uint256,address) => DISPATCHER(true)
    // getExchange(address) => NONDET

    // HUniswapV2
    addLiquidity(
        address tokenA,
        address tokenB,
        uint256 amountADesired,
        uint256 amountBDesired,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    ) => DISPATCHER(true)

    addLiquidityETH(
        address token,
        uint256 amountTokenDesired,
        uint256 amountTokenMin,
        uint256 amountETHMin,
        address to,
        uint256 deadline
    ) => DISPATCHER(true)

    removeLiquidity(
        address tokenA,
        address tokenB,
        uint256 liquidity,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    ) => DISPATCHER(true)

    removeLiquidityETH(
        address token,
        uint256 liquidity,
        uint256 amountTokenMin,
        uint256 amountETHMin,
        address to,
        uint256 deadline
    ) => DISPATCHER(true)

    swapExactTokensForTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] path,
        address to,
        uint256 deadline
    ) => DISPATCHER(true)

    swapTokensForExactTokens(
        uint256 amountOut,
        uint256 amountInMax,
        address[] path,
        address to,
        uint256 deadline
    ) => DISPATCHER(true)

    swapExactETHForTokens(
        uint256 amountOutMin,
        address[] path,
        address to,
        uint256 deadline
    ) => DISPATCHER(true)

    swapTokensForExactETH(
        uint256 amountOut,
        uint256 amountInMax,
        address[] path,
        address to,
        uint256 deadline
    ) => DISPATCHER(true)

    swapExactTokensForETH(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] path,
        address to,
        uint256 deadline
    ) => DISPATCHER(true)

    swapETHForExactTokens(
        uint256 amountOut,
        address[] path,
        address to,
        uint256 deadline
    ) => DISPATCHER(true)

    factory() => NONDET

    // HUniswapV3
    exactInputSingle((address,address,uint24,address,uint256,uint256,uint256,uint160))
        => DISPATCHER(true)
    exactInput((bytes,address,uint256,uint256,uint256))
        => DISPATCHER(true)
    exactOutputSingle((address,address,uint24,address,uint256,uint256,uint256,uint160))
        => DISPATCHER(true)
    exactOutput((bytes,address,uint256,uint256,uint256))
        => DISPATCHER(true)
    refundETH() => DISPATCHER(true)
    
    // HKyberNetwork
    // swapTokenToToken(address src, uint srcAmount, address dest, uint minConversionRate) 
    //     => DISPATCHER(true)
    // swapEtherToToken(address token, uint minConversionRate)
    //     => DISPATCHER(true)
    // swapTokenToEther(address token, uint srcAmount, uint minConversionRate)
    //     => DISPATCHER(true)

    // HBalancer
    exitPool(uint256 poolAmountIn, uint256[] minAmountsOut)
        => DISPATCHER(true)
    exitswapPoolAmountIn(address tokenOut, uint256 poolAmountIn, uint256 minAmountOut)
        => DISPATCHER(true)

    // HGasTokens
    freeFromUpTo(address,uint256) => DISPATCHER(true)

    // HMooniswap
    // deposit(uint256[] amounts, uint256[] minAmounts) returns(uint256)
    //     => DISPATCHER(true)
    // withdraw(uint256 amount, uint256[] minReturns)
    //     => DISPATCHER(true)
    // getTokens() => DISPATCHER(true)
    
    pools(address, address) => NONDET

    // HOneInchV3
    swap(address,(address,address,address,address,uint256,uint256,uint256,bytes),bytes) => DISPATCHER(true)
    unoswap(address,uint256,uint256,bytes32[]) => DISPATCHER(true)
    
    // HStakingRewardsToken
    stakingToken() => DISPATCHER(true)
    rewardsToken() => DISPATCHER(true)
    stakeFor(address account, uint256 amount) => DISPATCHER(true)
    withdrawFor(address account, uint256 amount) => DISPATCHER(true)
    getRewardFor(address account) => DISPATCHER(true)
    exitFor(address account) => DISPATCHER(true)
    isValid(address) => NONDET

    // HFurucomboStaking
    unstakeFor(address account, uint256 amount) => DISPATCHER(true)
    claimWeeks(address,(uint256,uint256,bytes32[])[]) => DISPATCHER(true)

    // HCToken, HCEther
    mint(uint256) => DISPATCHER(true)
    mint() => DISPATCHER(true)
    compoundredeem(uint256) => DISPATCHER(true)
    redeemUnderlying(uint256) => DISPATCHER(true)
    repayBorrowBehalf(address,uint256) => DISPATCHER(true)
    repayBorrowBehalf(address) => DISPATCHER(true)
    borrowBalanceCurrent(address) => DISPATCHER(true)
    underlying() => NONDET

    // HComptroller
    getCompAddress() => NONDET

    // HCurve
    exchange(
        int128 i,
        int128 j,
        uint256 dx,
        uint256 min_dy
    ) => DISPATCHER(true)
    exchange_underlying(
        int128 i,
        int128 j,
        uint256 dx,
        uint256 min_dy
    ) => DISPATCHER(true)
    add_liquidity(uint256[2] amounts, uint256 min_mint_amount)
        => DISPATCHER(true)
    add_liquidity(uint256[3] amounts, uint256 min_mint_amount)
        => DISPATCHER(true)
    add_liquidity(uint256[4] amounts, uint256 min_mint_amount)
        => DISPATCHER(true)
    add_liquidity(uint256[5] amounts, uint256 min_mint_amount)
        => DISPATCHER(true)
    add_liquidity(uint256[6] amounts, uint256 min_mint_amount)
        => DISPATCHER(true)
    add_liquidity(uint256[2] amounts, uint256 min_mint_amount, bool use_underlying)
        => DISPATCHER(true)
    add_liquidity(uint256[3] amounts, uint256 min_mint_amount, bool use_underlying)
        => DISPATCHER(true)
    add_liquidity(uint256[4] amounts, uint256 min_mint_amount, bool use_underlying)
        => DISPATCHER(true)
    add_liquidity(uint256[5] amounts, uint256 min_mint_amount, bool use_underlying)
        => DISPATCHER(true)
    add_liquidity(uint256[6] amounts, uint256 min_mint_amount, bool use_underlying)
        => DISPATCHER(true)
    remove_liquidity_one_coin(
        uint256 _token_amount,
        int128 i,
        uint256 min_amount
    ) => DISPATCHER(true)
    remove_liquidity_one_coin(
        uint256 _token_amount,
        int128 i,
        uint256 min_uamount,
        bool boolean
    ) => DISPATCHER(true)

    // HCurveDao
    mint_for(address,address) => DISPATCHER(true)
    deposit(uint256,address) => DISPATCHER(true)
    
    // HYVault
    deposit(uint256) => DISPATCHER(true)
    depositETH() => DISPATCHER(true)
    yvault_withdraw(uint256) => DISPATCHER(true)
    withdrawETH(uint256) => DISPATCHER(true)

    // HPolygon
    depositERC20ForUser(address,address,uint256) => DISPATCHER(true)
    depositFor(address,address,bytes) => DISPATCHER(true)
    depositEtherFor(address) => DISPATCHER(true)

    // HGelatoV2LimitOrder
    encodeEthOrder(address,address,address,address,bytes,bytes32) => DISPATCHER(true)
    depositEth(bytes) => DISPATCHER(true)

    // No-op for receiving funds without havocs
    nop() => NONDET
}

definition MAX_UINT256() returns uint256 = 115792089237316195423570985008687907853269984665640564039457584007913129639935
    ;

definition STACK_INCREASE_BOUND() returns uint256 = 1000000 ;    // 1 million

// ghost for checking if we touched the cache
ghost cacheTouched() returns bool;

hook Sstore cache[KEY bytes32 k] bytes32 value (bytes32 old_value) STORAGE {
    havoc cacheTouched assuming cacheTouched@new() == cacheTouched@old() || (value != old_value);
}

rule notTouchingCache(method f) {
    require !cacheTouched();
    arbitrary(f);
    assert !cacheTouched(), "Cache was touched maybe temporarily";
}


// should fail on all functions except maybe fallback.
rule sanity(method f) {
    arbitrary(f);
    assert false;
}

// if we start in a clear start state (flat slots) then we end in a clear start state
rule startStateCleanup(method f, uint slot) {
    uint oldValue = getSlot(slot);

    arbitrary(f);

    uint newValue = getSlot(slot);

    // slot 0 is stack length, which we ignore because some handlers are pushing entries into the stack
    assert oldValue == 0 => (newValue == 0 || slot == getStackLengthSlot()), "Start state of $slot which is not stack length was not cleaned up";
}

// if we start with a slot being non-zero then it should stay non-zero
// Status: currently violated on stack length overflow in execs.
rule noOverwrite(method f, uint slot) {
    require getStackLength() < MAX_UINT256() - STACK_INCREASE_BOUND(); // see stackLengthIncreaseIsBounded
    uint oldValue = getSlot(slot);

    arbitrary(f);

    uint newValue = getSlot(slot);
    
    // slot 0 is stack length, postProcess() may nullify it and it's fine, and execs() can increase it
    assert oldValue != 0 => (newValue == oldValue 
            || slot == getStackLengthSlot()), "Slot $slot changd during this execution";
}

// shows that the stack length increase is bounded. Selecting a reasonable bound gas-wise (and in any case bounded by the number of iterations of the loops)
rule stackLengthIncreaseIsBounded(method f) {
    uint256 stackLengthBefore = getStackLength();

    arbitrary(f);

    uint256 stackLengthAfter = getStackLength();
    assert stackLengthAfter <= stackLengthBefore + STACK_INCREASE_BOUND(), "Found a way to increase stack length by more than 1 million";
}

rule senderIsAlwaysCleanedUp(method f) {
    address before = getSender();

    arbitrary(f);

    address after = getSender();

    assert before == 0 => after == 0;
}

rule cubeCounterIsAlwaysCleanedUp(method f) {
    requireInvariant cubeCounterGreaterThan0IffSenderInitialized();
    uint256 before = getCubeCounter();

    arbitrary(f);

    uint256 after = getCubeCounter();

    assert before == 0 => after == 0;
}

rule cacheIsAlwaysCleanedUp(bytes32 key, method f) {
    // not cube counter or sender which take part in initialization
    require key != MSG_SENDER_KEY() && key != CUBE_COUNTER_KEY();
    bytes32 before = cache(key);

    arbitrary(f);

    bytes32 after = cache(key);

    assert before == 0 => after == 0;
}

rule nonExecutableWhenProxyIsBanned(method f) {
    require !isHandler();
    require !f.isView; // only non-view functions, that may modify the state, are interesting.
    env e;
    require registry.bannedAgents(currentContract) == 1; // proxy contract is banned

    calldataarg arg;
    f@withrevert(e, arg);
    assert lastReverted, "method invocation did not revert despite the contract has been banned in registry";
}

rule nonExecutableWhenHalted(method f) {
    require !isHandler();
    require !f.isView; // only non-view functions, that may modify the state, are interesting.
    require registry.fHalt(); // system is halted

    env e;
    calldataarg arg;
    f@withrevert(e, arg);
    assert lastReverted, "method invocation did not revert despite being called in a halted state";
}

rule nonExecutableWithUninitializedSender(method f) {
    require !isHandler();
    require !f.isView; // only non-view functions, that may modify the state, are interesting.
    require getSender() == 0; // no sender initialized;

    env e;
    calldataarg arg;
    f@withrevert(e, arg);
    assert (f.selector != proxy.batchExec(address[],bytes32[],bytes[]).selector/* && f.selector != certorafallback_0().selector*/ /* TODO */)
        => lastReverted, "method invocation did not revert despite being called without a set sender";
}

// if sender was initialized, and we have a callback, which functions fail? If they fail, it means they can't be callbacks
rule nonExecutableWithInitializedSender(method f) {
    require !isHandler();
    require !f.isView; // only non-view functions, that may modify the state, are interesting.
    require getSender() != 0; // sender is initialized

    env e;
    bool isGoodCaller = registry.isValidCaller(e, e.msg.sender);
    calldataarg arg;
    f@withrevert(e, arg);
    assert (f.isFallback && !isGoodCaller) => lastReverted; // only valid callers should execute in fallback successfully (would violate since certora prover cannot distinguish between receive and fallback for now)
    assert (f.selector == execs(address[],bytes32[],bytes[]).selector && e.msg.sender != currentContract) => lastReverted; // `execs` is allowed to be called by proxy itself after initialized
    assert (!f.isFallback && f.selector != execs(address[],bytes32[],bytes[]).selector) => lastReverted; // all non-view functions other than above ones should revert if sender is already initialized
}

// small havoc issue in batchExec, but getting coverage from execs() too.
rule transferredTokensMeanThatStackIsUpdated(method f) {
    require summaryInstance.getEthAddress(currentContract) != someToken; // not an eth transfer
    require someToken != 0; // not an eth transfer
    require someToken.allowance(currentContract, summaryInstance) == 0; // to make sure we're starting clean as implied by approvedTokensAreTemporary
    uint256 balanceBefore = someToken.balanceOf(currentContract);
    uint256 stackLengthBefore = getStackLength();
    require stackLengthBefore < MAX_UINT256() - STACK_INCREASE_BOUND(); // see stackLengthIncreaseIsBounded
    
    arbitrary(f);

    uint256 balanceAfter = someToken.balanceOf(currentContract);
    uint256 stackLengthAfter = getStackLength();
    
    assert (balanceAfter > balanceBefore) => stackLengthAfter > stackLengthBefore, 
        "must push an entry to postprocess stack if transferring funds into proxy which are not eth";
}

rule approvedTokensAreTemporary(method f, address someAllowed) {
    require summaryInstance.getEthAddress(currentContract) != someToken; // not an eth transfer
    require someToken != 0; // not an eth transfer
    require someAllowed == summaryInstance; // narrowing down
    uint256 allowanceBefore = someToken.allowance(currentContract, someAllowed);

    arbitrary(f);
    
    uint256 allowanceAfter = someToken.allowance(currentContract, someAllowed);

    assert allowanceBefore == 0 => allowanceAfter == 0, "Allowances must be nullified";
}

/*
    Each summary function will set a field describing if the results are as expected.
 */
rule tokenMovementCorrectness(method f) {
    storage initialStorage = lastStorage;
    require summaryInstance.consumedToken() == 0;
    require summaryInstance.generatedToken() == 0;
    require summaryInstance.erc20A() != summaryInstance.erc20B();
    
    env e;
    require e.msg.sender != 0; // 0 is reserved for minting/burning so we exclude it.
    require e.msg.sender != summaryInstance; // presumably, the DeFi protocol cannot invoke itself (Flashloan risk!)
    calldataarg arg;
    f(e, arg);

    address consumed = summaryInstance.consumedToken();
    address generated = summaryInstance.generatedToken();
    uint updatedConsumedTokenBalance = summaryInstance.getBalance(consumed, currentContract);
    uint updatedGeneratedTokenBalance = summaryInstance.getBalance(generated, currentContract);
    uint expectedConsumedAmount = summaryInstance.shouldBeConsumedAmount();
    uint origConsumedTokenBalance = summaryInstance.getBalance(consumed, currentContract) at initialStorage;
    uint origGeneratedTokenBalance = summaryInstance.getBalance(generated, currentContract);

    assert consumed != 0 => updatedConsumedTokenBalance == origConsumedTokenBalance - expectedConsumedAmount, "If there is a consumed token, should have consumed exactly the amount";
    assert (expectedConsumedAmount > 0 && generated != 0) => updatedGeneratedTokenBalance > origGeneratedTokenBalance, 
        "If consumed positive amount and expected to generate an amount, then should have generated a positive amount";
}

rule noOtherPartyModified(method f, address somebody) {
    require somebody != currentContract;
    require somebody != summaryInstance;
    require somebody != 0; // 0 is reserved for minting/burning so we exclude it.

    uint origTokenABalance = someToken.balanceOf(somebody);
    uint origTokenBBalance = someToken2.balanceOf(somebody);

    env e;
    require e.msg.sender != 0; // 0 is reserved for minting/burning so we exclude it.
    require e.msg.sender != summaryInstance; // presumably, the DeFi protocol cannot invoke itself (Flashloan risk!)
    calldataarg arg;
    f(e, arg);

    assert someToken.balanceOf(somebody) == origTokenABalance 
        && someToken2.balanceOf(somebody) == origTokenBBalance;
}

invariant cubeCounterGreaterThan0IffSenderInitialized() getCubeCounter() > 0 <=> getSender() != 0 {
    preserved {
        require getCubeCounter() < MAX_UINT256();
    }
}

/*
// the rule is usually expected to fail, because handler functions are payable.
rule holdNoEth(method f) {
    require ethBalance(currentContract) == 0;

    arbitrary(f);

    assert ethBalance(currentContract) == 0;
}

// the rule is usually expected to fail, because handler functions do not check who calls them (it's usually the sender via the proxy delegatecall).
rule onlyValidCaller(method f) {
    env e;
    bool isGoodCaller = registry.isValidCaller(e.msg.sender);
    calldataarg arg;
    f@withrevert(e, arg);
    bool succeeded = !lastReverted;

    assert !isGoodCaller => !succeeded, "function can be called even if the sender is not an allowed caller";
}
*/

function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}