using DummyERC20Impl as STAKED_TOKEN1

methods{
    STAKED_TOKEN1.balanceOf(address) returns(uint256) envfree
    totalSupply() returns(uint256) envfree
    onTransfer(address, address, uint256) => NONDET;
 }

// The holding token (stkAAVE) is always backed with a sufficient amount of the staked asset (AAVE)
invariant StkAaveIsBackedByAave()
    totalSupply() <= STAKED_TOKEN1.balanceOf(currentContract)
    {
        preserved with (env e){
            env e2; 
            require e.msg.sender != STAKED_TOKEN1;
            require e.msg.sender != currentContract;
            require REWARDS_VAULT(e2) != currentContract;
        }
    }
