/*
    @Invariant allSharesAreBacked
    @Description: Shares value cannot exceed actual locked amount of staked token
                  The update rewards functions are mutilated by returning
                  a NONDET value for _getRewards & _getAssetIndex . The reason for this
                  summarization is because the invariant does not claim anything about rewards.
    @Link: https://prover.certora.com/output/40577/370f63ee225743daba41087449111d8b/?anonymousKey=717499ff4fdcce2c8131025b4e00ade0e3a14200
*/
invariant allSharesAreBacked()
    previewRedeem(totalSupply()) <= stake_token.balanceOf(currentContract)
    {
        preserved stake(address to, uint256 amount) with (env e2)
        {
            require e2.msg.sender != currentContract;
        }
        preserved stakeWithPermit(address from, uint256 amount, uint256 deadline,
            uint8 v, bytes32 r, bytes32 s) with (env e3)
        {
            require from != currentContract;
        }
        preserved returnFunds(uint256 amount) with (env e4)
        {
            require e4.msg.sender != currentContract;
        }
        preserved initialize(address slashingAdmin, address cooldownPauseAdmin, address claimHelper,
                            uint256 maxSlashablePercentage, uint256 cooldownSeconds) with (env e5)
        {
            require getExchangeRate() == INITIAL_EXCHANGE_RATE();
        }
    }
