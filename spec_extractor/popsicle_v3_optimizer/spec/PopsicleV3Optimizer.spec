/*
* Scope of the project
- Verification of the main contract: PopsicleV3Optimizer.sol
* Out of the scope 
- All optimization calculations and math libraries
- Interaction with UniswapV3 pool
* UniswapV3pool simplified
- A simplified version of UniswapV3pool was developed specifically for this project
- SymbolicUniswapV3Pool.sol:
- functions mint(),collect(),burn(),swap(),observe(),tickSpacing(),slot0(),positions()
- Assumed : liquidity == balanced0 - owed0
*/ 
using DummyERC20A as token0
using DummyERC20B as token1
using SymbolicUniswapV3Pool as pool

////////////////////////////////////////////////////////////////////////////
//                      Methods                                           //
////////////////////////////////////////////////////////////////////////////

/*
    Declaration of methods that are used in the rules.
    envfree indicate that the method is not dependent on the environment (msg.value, msg.sender).
    Methods that are not declared here are assumed to be dependent on env.
*/
methods {
	//math functions
	floor(int24 tick, int24 tickSpacing) => NONDET
	getSqrtRatioAtTick(int24 tick) => NONDET
	getTickAtSqrtRatio(uint160 sqrtPriceX96) => NONDET
    sqrt(uint256 x) => approximateSqrt(x)
	// mulDiv(uint256 a, uint256 b, uint256 denominator) => NONDET
	mulDivRoundingUp(uint256 a, uint256 b, uint256 denominator) => NONDET
	
    
    getPositionTicks(address pool, uint256 amount0Desired, uint256 amount1Desired, int24 baseThreshold, int24 tickSpacing) => NONDET
	amountsForTicks(address pool, uint256 amount0Desired, uint256 amount1Desired, int24 _tickLower, int24 _tickUpper) => NONDET
	baseTicks(int24 currentTick, int24 baseThreshold, int24 tickSpacing) => NONDET
	amountsDirection(uint256 amount0Desired, uint256 amount1Desired, uint256 amount0, uint256 amount1) => NONDET
	checkDeviation(address pool, int24 maxTwapDeviation, uint32 twapDuration) => NONDET
	getTwap(address pool, uint32 twapDuration) => NONDET

	//interface IOptimizerStrategy 
    maxTotalSupply() => NONDET
    twapDuration() => NONDET
	maxTwapDeviation() => NONDET
	tickRangeMultiplier() => NONDET
	priceImpactPercentage() => NONDET

    balanceOf(address) returns(uint256) envfree
    totalSupply() returns(uint256) envfree

    //harness
    position_Liquidity() returns(uint128) envfree
    protocol_Liquidity() returns(uint128) envfree
    governance() returns(address) envfree
    protocolFees0() returns (uint256) envfree
    protocolFees1() returns (uint256) envfree
    totalFees0() returns (uint256) envfree
    totalFees1() returns (uint256) envfree
    token0.balanceOf(address) returns(uint256) envfree
    token1.balanceOf(address) returns(uint256) envfree
    pool.liquidity() returns (uint256) envfree
    pool.balance0() returns (uint256) envfree
    pool.balance1() returns (uint256) envfree
    pool.owed0() returns (uint128) envfree
    pool.owed1() returns (uint128) envfree
    

	// pool callback
	uniswapV3MintCallback(
        uint256 amount0,
        uint256 amount1,
        bytes data
    ) => DISPATCHER(true)

	uniswapV3SwapCallback(
        int256 amount0,
        int256 amount1,
        bytes  data
    ) => DISPATCHER(true)

}

ghost approximateSqrt(uint256) returns uint256;

////////////////////////////////////////////
/////////       Invariants
/////////////////////////////////////////////

    ////////////////////////////////////////////////
    ///// invariant balance_vs_protocol_Liquidity()
    ////  verifies that if total supply is zero than all the assets of the system is the owned to governance 
    ////  uniswapV3SwapCallback() - meaningless outside of the swap context
    ////  uniswapV3MintCallback() - meaningless outside of the mint context
    invariant balance_vs_protocol_Liquidity()
    (totalSupply() == 0) => token0.balanceOf(currentContract) == protocolFees0() //&&
                            //token1.balanceOf(currentContract) == protocolFees1()
    filtered { f -> f.selector != uniswapV3MintCallback(uint256,uint256,bytes).selector && f.selector != uniswapV3SwapCallback(int256,int256,bytes).selector }
        {
    preserved{
            require pool.owed0() % 5 == 0;
            require governance() != currentContract;
            require governance() != pool;

            requireInvariant empty_pool_state();
            requireInvariant zero_totalSupply_zero_owed();
            requireInvariant pool_balance_vs_owed();
            requireInvariant total_vs_protocol_Fees();
            requireInvariant liquidity_GE_poolBalance0();
            requireInvariant balance_contract_GE_protocolFees();
        }
    preserved withdraw(uint256 amount,address to) with (env e){
            require to != governance() && to != currentContract && to != pool;
            require e.msg.sender != currentContract && e.msg.sender != pool && e.msg.sender != governance();
         } 
    }
    
    ////////////////////////////////////////////////
    ///// invariant balance_contract_GE_protocolFees()
    ////  verifies that balance of the conttract is greater than protocol fees
    ////  uniswapV3SwapCallback() - meaningles outside of the swap context
    ////  uniswapV3MintCallback() - meaningles outside of the mint context
    invariant balance_contract_GE_protocolFees()
    token0.balanceOf(currentContract) >= protocolFees0()
    filtered { f -> f.selector != uniswapV3MintCallback(uint256,uint256,bytes).selector && f.selector != uniswapV3SwapCallback(int256,int256,bytes).selector }
    {
    preserved{
            require governance() != currentContract;
            require governance() != pool;

            requireInvariant empty_pool_state();
            requireInvariant zero_totalSupply_zero_owed();
            requireInvariant pool_balance_vs_owed();
            requireInvariant total_vs_protocol_Fees();
            requireInvariant liquidity_GE_poolBalance0();
        }
    preserved withdraw(uint256 amount,address to) with (env e){
        requireInvariant total_vs_protocol_Fees();
        require to != governance() && to != currentContract && to != pool;
        require e.msg.sender != currentContract && e.msg.sender != pool && e.msg.sender != governance();
         } 
    preserved deposit(uint256 amount0Desired,uint256 amount1Desired, address to) with (env e){
        require to != governance() && to != currentContract && to != pool;
        require e.msg.sender != currentContract && e.msg.sender != pool && e.msg.sender != governance();
        }
    } 

    ////////////////////////////////////////////////
    ///// invariant empty_pool_state()
    ////  verifies that pool liquidity == 0 IFF totalSupply == 0
    ////  collectProtocolFees() - it breakes the rule
    ////  uniswapV3MintCallback() - meaningless outside of the mint context
    invariant empty_pool_state()
    pool.liquidity() == 0 <=> totalSupply() == 0
    filtered { f -> excludeCallback(f) }
    {
    preserved {
            require governance() != currentContract;
            require governance() != pool;

            requireInvariant zero_totalSupply_zero_owed();
            requireInvariant pool_balance_vs_owed();
            requireInvariant total_vs_protocol_Fees();
            requireInvariant liquidity_GE_poolBalance0();
            requireInvariant balance_contract_GE_protocolFees();

         }   
    preserved withdraw(uint256 amount,address to) with (env e){
             require to != governance() && to != currentContract && to != pool;
             require e.msg.sender != currentContract && e.msg.sender != pool && e.msg.sender != governance();
         } 
    }

    ////////////////////////////////////////////////
    ///// invariant empty_pool_state_reverse()
    ////  verifies that pool liquidity == 0 IFF pool balance - pool owed == 0
    ////  following function are excluded:
    ////  collectProtocolFees() - it breakes the rule
    ////  uniswapV3MintCallback() - meaningless outside of the mint context
    invariant empty_pool_state_reverse()
    pool.liquidity() == 0 <=> (pool.balance0() - pool.owed0() == 0 && pool.balance1() - pool.owed1() == 0)
    filtered { f -> excludeCallback(f) }
    {            
    preserved{
            require governance() != currentContract;
            require governance() != pool;

            requireInvariant empty_pool_state();
            requireInvariant zero_totalSupply_zero_owed();
            requireInvariant pool_balance_vs_owed();
            requireInvariant total_vs_protocol_Fees();
            requireInvariant liquidity_GE_poolBalance0();
            requireInvariant balance_contract_GE_protocolFees();
        }
    preserved withdraw(uint256 amount,address to) with (env e){
            require to != currentContract && to != pool && to != governance() ;
            require e.msg.sender != currentContract && e.msg.sender != pool && e.msg.sender != governance();
         } 
    preserved deposit(uint256 amount0Desired,uint256 amount1Desired, address to) with (env e){
            require to != currentContract && to != pool && to != governance();
            require e.msg.sender != currentContract && e.msg.sender != pool && e.msg.sender != governance();
         } 
    }
    ////////////////////////////////////////////////
    ///// invariant zero_totalSupply_zero_owed()
    ////  verifies that all assets withdrawn - totalSupply == 0 - no owed assets left in the pool
    invariant zero_totalSupply_zero_owed()
    totalSupply() == 0 => (pool.owed0() == 0 && pool.owed1() == 0){ 
    preserved {
        requireInvariant empty_pool_state();
    } 
    }
    
    ////////////////////////////////////////////////
    ///// invariant pool_balance_vs_owed()
    ////  verifies that pool balance greater equal to pool owed
    ////  uniswapV3MintCallback() - meaningless outside of the mint context
    invariant pool_balance_vs_owed()
    pool.balance0() >= pool.owed0() && pool.balance1() >= pool.owed1()
    filtered { f -> excludeCallback(f) }

    ////////////////////////////////////////////////
    ///// invariant zero_pool_balance_zero_owed()
    ////  verifies that pool balance == 0 implies pool owed == 0
    ////  uniswapV3MintCallback() - meaningless outside of the mint context
    invariant zero_pool_balance_zero_owed()
    (pool.balance0() == 0 => pool.owed0() == 0) && 
    (pool.balance1() == 0 => pool.owed1() == 0)
    filtered { f -> excludeCallback(f) }

    ////////////////////////////////////////////////
    ///// invariant total_vs_protocol_Fees()
    ////  verifies that total fees greater than protocol fees
    invariant total_vs_protocol_Fees()
    totalFees0() > protocolFees0() ||
    totalFees0() == 0 &&  protocolFees0() == 0
    {
        preserved deposit(uint256 amount0Desired,uint256 amount1Desired, address to) with (env e){
             require to != currentContract && to != pool && to != governance();
             require e.msg.sender != currentContract && e.msg.sender != pool && e.msg.sender != governance();
         } 
    }

    ////////////////////////////////////////////////
    ///// invariant liquidity_GE_poolBalance0()
    ////  verifies that pool liquidity == pool balance - pool owed
    ////  collectProtocolFees() - breaks the rule
    ////  uniswapV3MintCallback() - meaningless outside of the mint context
    invariant liquidity_GE_poolBalance0()
    pool.liquidity() == pool.balance0() - pool.owed0()
    filtered { f -> excludeCallback(f) }
    {
    preserved{
            require governance() != currentContract;
            require governance() != pool;

            requireInvariant empty_pool_state();
            requireInvariant zero_totalSupply_zero_owed();
            requireInvariant pool_balance_vs_owed();
            requireInvariant total_vs_protocol_Fees();
            requireInvariant balance_contract_GE_protocolFees();
        }
    preserved withdraw(uint256 amount,address to) with (env e){
            require to != currentContract && to != pool && to != governance();
            require e.msg.sender != currentContract && e.msg.sender != pool && e.msg.sender != governance();
         } 
    }

    definition excludeCallback(method f) returns bool = f.selector != uniswapV3MintCallback(uint256,uint256,bytes).selector && f.selector != uniswapV3SwapCallback(int256,int256,bytes).selector;

////////////////////////////////////////////
/////////       Rules
/////////////////////////////////////////////


////////////////////////////////////////////////
///// rule zeroCharacteristicOfWithdraw()
////  verifies that if withraw returns amount0 == 0 and amount1 == 0 then necessarily shares == 0
rule zeroCharacteristicOfWithdraw(uint256 shares, address to){
    env e;
    uint256 amount0;
    uint256 amount1;

    require governance() != currentContract;
    require governance() != pool;
    require to != currentContract && to != pool && to != governance();
    require e.msg.sender != currentContract && e.msg.sender != pool && e.msg.sender != governance();

    amount0,amount1 =  withdraw(e,shares, to);

    assert (amount0 == 0 && amount1 == 0 => shares == 0);
}
////////////////////////////////////////////////
///// rule more_shares_more_amounts_to_withdraw()
////  verifies that with larger number of shares one will withdraw a larger amount of assets
////  this rule passes only when the following line added to burnLiquidityShares():
////  require (share == liquidity * totalSupply/uint256(liquidityInPool));
// rule more_shares_more_amounts_to_withdraw( address to){
// env e;
//     uint256 sharesX;
//     uint256 sharesY;
//     uint256 amount0X;
//     uint256 amount1X;
//     uint256 amount0Y;
//     uint256 amount1Y;

//     require governance() != currentContract;
//     require governance() != pool;
//     require to != currentContract && to != pool && to != governance();
//     require e.msg.sender != currentContract && e.msg.sender != pool && e.msg.sender != governance();

//     require sharesX > sharesY;
//     storage init = lastStorage;
    
//     amount0X,amount1X =  withdraw(e,sharesX, to);
//     amount0Y,amount1Y =  withdraw(e,sharesY, to) at init;
    

//     assert amount0X >= amount0Y && amount1X >= amount1Y;
// }
////////////////////////////////////////////////
///// rule totalSupply_vs_positionAmounts()
////  verifies that totalSupply before applying f() greater than totalSupply after implies posistion 
////  liquidity before is greater than position liquidity after minus last compound liquidity
rule totalSupply_vs_positionAmounts(method f){
   env e;

   uint256 totalSupplyBefore = totalSupply();
   uint256 posLiquidityBefore = position_Liquidity();

    require governance() != currentContract;
    require governance() != pool;

   require lastCompoundLiquidity(e) == 0;

   calldataarg args;
	f(e,args);

   uint256 totalSupplyAfter = totalSupply();
   uint256 posLiquidityAfter = position_Liquidity();   
   uint256 compoundAfter = lastCompoundLiquidity(e);

    assert totalSupplyAfter < totalSupplyBefore =>
            posLiquidityAfter - compoundAfter < posLiquidityBefore;
}
////////////////////////////////////////////////
///// rule protocolFees_state()
////  verifies that balance of governance before applying f() + the change in protocolFees is greater or equal balance of governance after applying f()
////  uniswapV3SwapCallback() - meaningless outside of the swap context
////  uniswapV3MintCallback() - meaningless outside of the mint context
////  acceptGovernance()      - breaks the rule when governance changes
rule protocolFees_state(env e, method f, uint256 shares, address to)
    filtered { f -> f.selector != uniswapV3MintCallback(uint256,uint256,bytes).selector && f.selector != uniswapV3SwapCallback(int256,int256,bytes).selector && f.selector != acceptGovernance().selector }
{
    require governance() != currentContract;
    require governance() != pool;
    require pool.owed0() == 0;
    requireInvariant  total_vs_protocol_Fees();
        
    uint256 balanceGovBefore = token0.balanceOf(governance());
    uint256 balanceProBefore = protocolFees0();
        
    calldataarg args;
    if (f.selector==withdraw(uint256,address).selector){
        require(to!=governance());
        withdraw(e,shares, to);
    }
    else {
	    f(e,args);
    }
        
    uint256 balanceGovAfter = token0.balanceOf(governance());
    uint256 balanceProAfter = protocolFees0();
    uint256 proChange = balanceProAfter > balanceProBefore ? balanceProAfter - balanceProBefore : balanceProBefore - balanceProAfter;

    assert balanceGovAfter <= balanceGovBefore + proChange;
}
    
////////////////////////////////////////////////
///// rule empty_pool_zero_totalSupply()
////  verifies that pool is empty IFF totalSupply == 0
////  uniswapV3MintCallback() - meaningless outside of the mint context
////  collectProtocolFees() - it breakes the rule
rule empty_pool_zero_totalSupply(method f, address to)
filtered { f -> excludeCallback(f) }{
    env e;

    require governance() != currentContract;
    require governance() != pool;
    require (pool.balance0() - pool.owed0() == 0 && pool.balance1() - pool.owed1() == 0 ) <=> totalSupply() == 0;
    require (to!=governance() && to != pool && to != currentContract);
    
    requireInvariant empty_pool_state();
    requireInvariant zero_totalSupply_zero_owed();
    requireInvariant pool_balance_vs_owed();
    requireInvariant total_vs_protocol_Fees();
    requireInvariant liquidity_GE_poolBalance0();
    requireInvariant balance_contract_GE_protocolFees();

    calldataarg args;
    if (f.selector==withdraw(uint256,address).selector){
        uint256 shares;
        require e.msg.sender != pool && e.msg.sender != currentContract && e.msg.sender != governance();
        require shares == totalSupply();
        require to != governance();
        withdraw(e,shares, to);
        require pool.balance0() - pool.owed0() == 0 && pool.balance1() - pool.owed1() == 0 ;
    }
    else         
    if (f.selector==deposit(uint256,uint256,address).selector){
        uint256 amount0Desired;
        uint256 amount1Desired;
        require e.msg.sender != pool && e.msg.sender != currentContract && e.msg.sender != governance();
        deposit(e,amount0Desired,amount1Desired,to);
    }
    else {
	    f(e,args);
    }
    assert (pool.balance0() - pool.owed0() == 0 && pool.balance1() - pool.owed1() == 0 ) <=> totalSupply() == 0;
}

// rule withdraw_amount(address to){
//     env e;

//     require governance() != currentContract;
//     require governance() != pool;
//     require (to!=governance() && to != pool && to != currentContract);
//     require e.msg.sender != pool && e.msg.sender != currentContract && e.msg.sender != governance();

//     require token0.balanceOf(currentContract) == 0 &&
//             token1.balanceOf(currentContract) == 0;

//             requireInvariant empty_pool_state();
//             requireInvariant zero_totalSupply_zero_owed();
//             requireInvariant pool_balance_vs_owed();
//             requireInvariant total_vs_protocol_Fees();
//             requireInvariant liquidity_GE_poolBalance0();
//             requireInvariant balance_contract_GE_protocolFees();

//     uint256 shares;
//     uint256 amount0;
//     uint256 amount1;

//     uint256 totalsupply = totalSupply();
//     uint256 pool_balance0 = pool.balance0();
//     uint256 pool_owed0 = pool.owed0();

//             amount0,amount1 =  withdraw(e,shares, to);
    
//     // uint256 amount0_calc = (pool_balance0 - pool_owed0) * shares / totalsupply;
//     mathint amount0_calc = pool_balance0 * shares / totalsupply;
//     require amount0_calc >= 1;

//     assert  amount0 <= amount0_calc;
// }
// after calling rebalance, token0.balanceOf(this)==0 and token1.balanceOf(this)==0
/* rule zeroBalancesAfterRebalance(){
    env e;
    rebalance(e);
    assert (token0.balanceOf(e, currentContract)==0 && 
                             token1.balanceOf(e, currentContract)==0);
} */

/*
    ghost sumAllBalances() returns uint256 {
    init_state axiom sumAllBalances() == 0;
}


// the hook that updates the ghost function as follows
// "At every write to the value at key 'a' in 'balances'
// increase ghostTotalSupply by the difference between
// tho old value and the new value"
//                              the new value ↓ written:
 hook Sstore _balances[KEY address a] uint256 balance
// the old value ↓ already there
    (uint256 old_balance) STORAGE {
  havoc sumAllBalances assuming sumAllBalances@new() == sumAllBalances@old() +
      (balance - old_balance);
}

 hook Sload uint256 balance _balances[KEY address a] STORAGE {
     require balance <= sumAllBalances();
 }

    invariant totalSupplyIntegrity() 
    totalSupply() == sumAllBalances()
  