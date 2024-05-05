using Registry as registry
using DummyERC20A as someToken
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
    handlers(address) returns (bytes32) envfree => DISPATCHER(true)
    callers(address) returns (bytes32) envfree => DISPATCHER(true)
    bannedAgents(address) returns (uint256) envfree => DISPATCHER(true)
    fHalt() returns (bool) envfree => DISPATCHER(true)
    owner() returns (address) envfree => DISPATCHER(true)
    isValidCaller(address) returns (bool) envfree => DISPATCHER(true)
    isValidHandler(address) returns (bool) => DISPATCHER(true)

    // for abstracting exec of handler
    0x12345678 => NONDET

    // ERC20
    transfer(address,uint256) => DISPATCHER(true)
    transferFrom(address,address,uint256) => DISPATCHER(true)
    approve(address,uint256) => DISPATCHER(true)
    allowance(address,address) returns (uint) envfree => DISPATCHER(true)
    balanceOf(address) returns (uint) envfree => DISPATCHER(true)
    totalSupply() returns (uint) envfree => DISPATCHER(true)

    havocMe(address) => DISPATCHER(true)
    havocMeEth() => DISPATCHER(true)

    summaryInstance.lenDelegated() returns (uint256) envfree
    summaryInstance.checkDelegated(address) returns (bool) envfree

    execute(address,bytes) returns (bytes32) => DISPATCHER(true) // should modify/havoc erc20 balances. The returns part is super important for soundness!

    // HSCompound
    claimComp(address) => DISPATCHER(true) 
    FCOMPOUND_ACTIONS() returns (address) envfree

    // WETH
    withdraw(uint256) => DISPATCHER(true)
    
    // No-op for receiving funds without havocs
    nop() => NONDET
}

// Guarantee execute() gets only an authorized address
rule executeDelegatesOnlyToAllowedAddresses(method f) {
    require summaryInstance.lenDelegated() == 0;

    arbitrary(f);

    uint pushed = summaryInstance.lenDelegated();
    assert pushed <= 3, "not expected to call execute more than 3 times";
    assert summaryInstance.checkDelegated(FCOMPOUND_ACTIONS()), "not all delegated are allowed";
}

function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}