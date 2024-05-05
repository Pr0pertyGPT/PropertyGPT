methods {
	getSqrtRatioAtTick(int24) => NONDET
	getTickAtSqrtRatio(uint160) => NONDET
	floor(int24 tick, int24 tickSpacing) => NONDET
}

	

rule sanity(method f) filtered { f -> !f.isView }  {
	env e;
	calldataarg args;
	f(e,args);
	assert(false);
}


rule sanityForView(method f) filtered { f -> f.isView }  {
	env e;
	calldataarg args;
	f(e,args);
	assert(false);
}


// rule reentrency(method f) filtered { f -> !f.isView } {
// 	env e;
// 	calldataarg args;
// 	require _status(e) == 2;
// 	f@withrevert(e,args);
// 	assert lastReverted; 
// }

/*
amountsForLiquidity(pool, totalSupply()
        uint128 liquidity,
        int24 _tickLower,
        int24 _tickUpper
    )
	*/