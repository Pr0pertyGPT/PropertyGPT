
# Properties: 

      balances[user] <= totalSupply()

      ghost that proves sums(balances) == totalSupply

  ## montonicity : Gadi
      totalSupply decrease <=> positionAmounts(pool, tickLower, tickUpper) decrease

  ## validity of total supply : Gadi
      totalSupply <=  positionLiquidity - protocolLiquidity


 ## reentrency


  ## total assets of user: totalAssetsOfUser commented out
  ## total assets of user:
      earnfees
      compoundfees
        (amount0, amount1) = positionAmounts(pool, tickLower, tickUpper)
        (protocol0, protocol1) = amountsForLiquidity(pool, protocolFee0, _tickLower, _tickUpper)
        usersAmount0 = amount0 - protocolFees0
        token0.balanceOf(user) +  usersAmount0 * balanceOf[user] / totalSupply() 
        
// f - external
        Should stay the same on external functions

        Should stay the same on all functions

       

  ## additivity of withdraw : written, fails, reviewed 

        ** we think this breaks on _compoundFees in case when the pool.mint returns values less than the current balance 


  ## additivity of withdraw 
        Withdraw (shareX, msg.sender) ; Withdraw(shareY, msg.sender) == Withdraw (shareX + shareY, msg.sender)

        balanceof[msg.sender] >= shareX + shareY 
        token0.balanceOf[msg.sender]
        token1.balanceOf[msg.sender]

      

    
  ## front running on withdraw (this broke but looks like fixed now): written, fails, need review
        withdrawing the same amount at the same block yields the same token amounts 
            withdraw@user1(share, user1) ; withdraw@user2(share, user2) 
                token0.balanceOf[user1] ==  token0.balanceOf[user2]
                token1.balanceOf[user1] ==  token1.balanceOf[user2] 
 

  ## zero characteristic  Gadi
      withdraw(shares) == (0,0)   =>  share ==  0


  ## solvency of the system  - written, fails, need review 
         
        (amount0, amount1) = positionAmounts(pool, tickLower, tickUpper)
        usersAmount0 = amount0 - protocolFees0
        amountInUniswapPerShare0 = usersAmount0 / totalSupply()

        amountInUniswapPerShare should stay the same on withdraw, deposit, ERC20 functions  if no fee collected if ratio didn't change

        if fees collected amountInUniswapPerShare can only increase    

        amountInUniswapPerShare0 anti-monotonicity amountInUniswapPerShare1 (because of swap and flashloans )
        

  ## rules on protocolFees
         reduced only on collectProtocolFee
         protocolFees0 can increase by 10% of current action 

        collectProtocolFee()
        protocolFees0 = 0; 
        f() /* withdraw, deposit, ... */
        assert ( protocolfee < 10% for fees by pook(0)
        

 
  ## impact by uniswap
     first deposit or swap with flashloan to uniswap and optimizer will be effected 

// rule about rebalance:
after calling rebalance, token0.balanceOf(this)==0 and token1.balanceOf(this)==0

// fix to solvency of the system: the ratio of token0 and token1 can change so // the share price must be calculated by liquidty
    liquidity = positionLiqudity(pool, tickLower, tickUpper)
    usersLiquidty = liquidity - protocolLiquidity
    amountInUniswapPerShare = userLiquidity / totalSupply()

    amountInUniswapPerShare should stay the same on withdraw, deposit, ERC20 functions    

// rules on protocolFees:
oldLiquidity=positionLiqudity(pool, tickLower, tickUpper)
oldProtolLiquidity=pool.liquidityForAmounts(protocolFees0, protocolFees1, tickLower, tickUpper)
swap(…)
_earnFees()
_compundFees()
newLiquidity=positionLiqudity(pool, tickLower, tickUpper)
assert (pool.liquidityForAmounts(protocolFees0, protocolFees1, tickLower, tickUpper)-oldProtocolLiquidity)*10==newLiquidity-oldLiquidty
