import "../helpers/erc20.spec"

// using JoeFactory as Factory

methods{
    mint(address) returns uint256 => DISPATCHER(true)
    getPair(address, address) returns address envfree => DISPATCHER(true)
    feeTo() returns address => DISPATCHER(true)
    getReserves() returns uint112, uint112, uint32 => DISPATCHER(true)
    createPair(address, address) returns address => DISPATCHER(true)
    migrator() returns address => DISPATCHER(true)
    initialize(address, address) => DISPATCHER(true)
    newPair() returns address => NONDET
    desiredLiquidity()returns uint256 => NONDET     // in JoePair contract 
}

rule sanity(method f)
{
	env e;
	calldataarg args;
	f(e,args);
	assert false;
}
