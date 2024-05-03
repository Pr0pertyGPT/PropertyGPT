methods {
    handlers(address) returns (bytes32) envfree
    callers(address) returns (bytes32) envfree
    bannedAgents(address) returns (uint256) envfree
    owner() returns (address) envfree
}

definition deprecated() returns bytes32 = 0x6465707265636174656400000000000000000000000000000000000000000000;

function handlerTransition(address handler, bytes32 before, bytes32 after, method f) {
    require before == handlers(handler);
    callArbitrary(f);
    require after == handlers(handler);
}

function callerTransition(address caller, bytes32 before, bytes32 after, method f) {
    require before == callers(caller);
    callArbitrary(f);
    require after == callers(caller);
}

rule changesHandler(method f, address handler) {
    bytes32 _regState;
    bytes32 regState_;
    handlerTransition(handler, _regState, regState_, f);
    assert (f.selector != register(address,bytes32).selector && f.selector != unregister(address).selector) 
        => _regState == regState_, "method unexpectedly changes handler info";
}

rule deprecatesHandler(method f, address handler) {
    bytes32 _regState;
    bytes32 regState_;
    handlerTransition(handler, _regState, regState_, f);
    assert (f.selector != unregister(address).selector) 
        => _regState != deprecated() /* non deprecated */ => regState_ != deprecated(), "method unexpectedly deprecates handler";
}

rule changesCaller(method f, address caller) {
    bytes32 _regState;
    bytes32 regState_;
    callerTransition(caller, _regState, regState_, f);
    assert (f.selector != registerCaller(address,bytes32).selector && f.selector != unregisterCaller(address).selector) 
        => _regState == regState_, "method unexpectedly changes caller info";
}

rule deprecatesCaller(method f, address caller) {
    bytes32 _regState;
    bytes32 regState_;
    callerTransition(caller, _regState, regState_, f);
    assert (f.selector != unregisterCaller(address).selector) 
        => _regState != deprecated() /* non deprecated */ => regState_ != deprecated(), "method unexpectedly deprecates caller";
}

rule unregisterHandlerIsPermanent(method f, address handler) {
    env e;
    unregister(e, handler);

    callArbitrary(f);

    assert handlers(handler) == deprecated(), "unexpected handler info after unregister";
}

rule unregisterCallerIsPermanent(method f, address caller) {
    env e;
    unregisterCaller(e, caller);

    callArbitrary(f);

    assert callers(caller) == deprecated(), "unexpected caller info after unregister";
}

rule unregisterHandlerIsPermanent2(method f, address handler) {
    require handlers(handler) == deprecated();

    callArbitrary(f);

    assert handlers(handler) == deprecated(), "unexpected handler info after unregister";
}

rule unregisterCallerIsPermanent2(method f, address caller) {
    require callers(caller) == deprecated();

    callArbitrary(f);

    assert callers(caller) == deprecated(), "unexpected caller info after unregister";
}

rule banningIsReversible(address agent, method f) {
    require owner() != 0;
    env e;
    ban(e, agent);

    // call some function for covering more cases
    require f.selector != unban(address).selector;
    callArbitrary(f);

    env e2;
    require e2.msg.value == 0;
    require e2.msg.sender == e.msg.sender;
    unban@withrevert(e2, agent);
    assert !lastReverted, "Unbanning should succeed";
}

rule haltingIsReversible(method f) {
    require owner() != 0;
    env e;
    halt(e);

    // call some function for covering more cases
    require f.selector != unhalt().selector;
    callArbitrary(f);

    env e2;
    require e2.msg.value == 0;
    require e2.msg.sender == e.msg.sender;
    assert e.msg.sender != 0, "Cannot send transactions from 0 address";
    unhalt@withrevert(e2);
    assert !lastReverted, "Unhalting should succeed";
}

function callArbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}