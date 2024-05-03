import "erc20.spec"

methods {
    underlying() returns(address) envfree
    underlyingTotalSupply() returns(uint256) envfree
    underlyingBalanceOf(address) returns(uint256) envfree

    depositFor(address, uint256) returns(bool)
    withdrawTo(address, uint256) returns(bool)
    _recover(address) returns(uint256)
}


// STATUS - verified
// totalsupply of wrapped should be less than or equal to underlying (assuming no external transfer) - solvency
invariant whatAboutTotal(env e)
    totalSupply(e) <= underlyingTotalSupply()
    filtered { f -> f.selector != certorafallback_0().selector && !f.isView}
    {
        preserved {
            require underlyingBalanceOf(currentContract) <= underlyingTotalSupply();
        }
        preserved depositFor(address account, uint256 amount) with (env e2){
            require totalSupply(e) + amount <= underlyingTotalSupply();
        }
    }


// STATUS - verified
// totalsupply of wrapped should be less than or equal to the underlying balanceOf contract (assuming no external transfer) - solvency
invariant underTotalAndContractBalanceOfCorrelation(env e)
    totalSupply(e) <= underlyingBalanceOf(currentContract)
    {
        preserved with (env e2) {
            require underlying() != currentContract;
            require e.msg.sender != currentContract;
            require e.msg.sender == e2.msg.sender;
        }
    }


// STATUS - verified
// Check that values are updated correctly by `depositFor()`
rule depositForSpecBasic(env e){
    address account; uint256 amount;

    require e.msg.sender != currentContract;
    require underlying() != currentContract;

    uint256 wrapperTotalBefore = totalSupply(e);
    uint256 underlyingTotalBefore = underlyingTotalSupply();
    uint256 underlyingThisBalanceBefore = underlyingBalanceOf(currentContract);

    depositFor(e, account, amount);

    uint256 wrapperTotalAfter = totalSupply(e);
    uint256 underlyingTotalAfter = underlyingTotalSupply();
    uint256 underlyingThisBalanceAfter = underlyingBalanceOf(currentContract);

    assert wrapperTotalBefore == wrapperTotalAfter - amount, "wrapper total wrong update";
    assert underlyingTotalBefore == underlyingTotalAfter, "underlying total was updated";
    assert underlyingThisBalanceBefore == underlyingThisBalanceAfter - amount, "underlying this balance wrong update";
}


// STATUS - verified
// Check that values are updated correctly by `depositFor()`
rule depositForSpecWrapper(env e){
    address account; uint256 amount;

    require underlying() != currentContract;

    uint256 wrapperUserBalanceBefore = balanceOf(e, account);
    uint256 wrapperSenderBalanceBefore = balanceOf(e, e.msg.sender);

    depositFor(e, account, amount);

    uint256 wrapperUserBalanceAfter = balanceOf(e, account);
    uint256 wrapperSenderBalanceAfter = balanceOf(e, e.msg.sender);

    assert account == e.msg.sender => wrapperUserBalanceBefore == wrapperSenderBalanceBefore 
                && wrapperUserBalanceAfter == wrapperSenderBalanceAfter 
                && wrapperUserBalanceBefore == wrapperUserBalanceAfter - amount, "wrapper balances wrong update";
    assert account != e.msg.sender => wrapperUserBalanceBefore == wrapperUserBalanceAfter - amount
                && wrapperSenderBalanceBefore == wrapperSenderBalanceAfter, "wrapper balances wrong update";
}


// STATUS - verified
// Check that values are updated correctly by `depositFor()`
rule depositForSpecUnderlying(env e){
    address account; uint256 amount;

    require e.msg.sender != currentContract;
    require underlying() != currentContract;

    uint256 underlyingSenderBalanceBefore = underlyingBalanceOf(e.msg.sender);
    uint256 underlyingUserBalanceBefore = underlyingBalanceOf(account);

    depositFor(e, account, amount);

    uint256 underlyingSenderBalanceAfter = underlyingBalanceOf(e.msg.sender);
    uint256 underlyingUserBalanceAfter = underlyingBalanceOf(account);

    assert account == e.msg.sender => underlyingSenderBalanceBefore == underlyingUserBalanceBefore
                && underlyingSenderBalanceAfter == underlyingUserBalanceAfter
                && underlyingSenderBalanceBefore == underlyingSenderBalanceAfter + amount, "underlying balances wrong update";
    
    assert account != e.msg.sender && account == currentContract => underlyingSenderBalanceBefore == underlyingSenderBalanceAfter + amount
                && underlyingUserBalanceBefore == underlyingUserBalanceAfter - amount, "underlying balances wrong update";
    
    assert account != e.msg.sender && account != currentContract => underlyingSenderBalanceBefore == underlyingSenderBalanceAfter + amount
                && underlyingUserBalanceBefore == underlyingUserBalanceAfter, "underlying balances wrong update";
}


// STATUS - verified
// Check that values are updated correctly by `withdrawTo()`
rule withdrawToSpecBasic(env e){
    address account; uint256 amount;

    require underlying() != currentContract;

    uint256 wrapperTotalBefore = totalSupply(e);
    uint256 underlyingTotalBefore = underlyingTotalSupply();

    withdrawTo(e, account, amount);

    uint256 wrapperTotalAfter = totalSupply(e);
    uint256 underlyingTotalAfter = underlyingTotalSupply();

    assert wrapperTotalBefore == wrapperTotalAfter + amount, "wrapper total wrong update";
    assert underlyingTotalBefore == underlyingTotalAfter, "underlying total was updated";
}


// STATUS - verified
// Check that values are updated correctly by `withdrawTo()`
rule withdrawToSpecWrapper(env e){
    address account; uint256 amount;

    require underlying() != currentContract;

    uint256 wrapperUserBalanceBefore = balanceOf(e, account);
    uint256 wrapperSenderBalanceBefore = balanceOf(e, e.msg.sender);

    withdrawTo(e, account, amount);

    uint256 wrapperUserBalanceAfter = balanceOf(e, account);
    uint256 wrapperSenderBalanceAfter = balanceOf(e, e.msg.sender);
    
    assert account == e.msg.sender => wrapperUserBalanceBefore == wrapperSenderBalanceBefore
                && wrapperUserBalanceAfter == wrapperSenderBalanceAfter
                && wrapperUserBalanceBefore == wrapperUserBalanceAfter + amount, "wrapper user balance wrong update";
    assert account != e.msg.sender => wrapperSenderBalanceBefore == wrapperSenderBalanceAfter + amount
                && wrapperUserBalanceBefore == wrapperUserBalanceAfter, "wrapper user balance wrong update";
}


// STATUS - verified
// cCheck that values are updated correctly by `withdrawTo()`
rule withdrawToSpecUnderlying(env e){
    address account; uint256 amount;

    require e.msg.sender != currentContract;
    require underlying() != currentContract;

    uint256 underlyingSenderBalanceBefore = underlyingBalanceOf(e.msg.sender);
    uint256 underlyingUserBalanceBefore = underlyingBalanceOf(account);
    uint256 underlyingThisBalanceBefore = underlyingBalanceOf(currentContract);

    withdrawTo(e, account, amount);

    uint256 underlyingSenderBalanceAfter = underlyingBalanceOf(e.msg.sender);
    uint256 underlyingUserBalanceAfter = underlyingBalanceOf(account);
    uint256 underlyingThisBalanceAfter = underlyingBalanceOf(currentContract);

    assert account == e.msg.sender => underlyingSenderBalanceBefore == underlyingUserBalanceBefore 
                && underlyingSenderBalanceAfter == underlyingUserBalanceAfter 
                && underlyingUserBalanceBefore == underlyingUserBalanceAfter - amount, "underlying balances wrong update (acc == sender)";
    
    assert account != e.msg.sender && account == currentContract => underlyingUserBalanceBefore == underlyingUserBalanceAfter
                && underlyingSenderBalanceBefore == underlyingSenderBalanceAfter, "underlying balances wrong update (acc == contract)"; 
    assert account != e.msg.sender && account != currentContract => underlyingUserBalanceBefore == underlyingUserBalanceAfter - amount
                && underlyingSenderBalanceBefore == underlyingSenderBalanceAfter
                && underlyingThisBalanceBefore == underlyingThisBalanceAfter + amount, "underlying balances wrong update (acc != contract)";   
}


// STATUS - verified
// Check that values are updated correctly by `_recover()`
rule recoverSpec(env e){
    address account; uint256 amount;

    uint256 wrapperTotalBefore = totalSupply(e);
    uint256 wrapperUserBalanceBefore = balanceOf(e, account);
    uint256 wrapperSenderBalanceBefore = balanceOf(e, e.msg.sender);
    uint256 underlyingThisBalanceBefore = underlyingBalanceOf(currentContract);

    mathint value = underlyingThisBalanceBefore - wrapperTotalBefore;

    _recover(e, account);

    uint256 wrapperTotalAfter = totalSupply(e);
    uint256 wrapperUserBalanceAfter = balanceOf(e, account);
    uint256 wrapperSenderBalanceAfter = balanceOf(e, e.msg.sender);
    
    assert wrapperTotalBefore == wrapperTotalAfter - value, "wrapper total wrong update";
    assert e.msg.sender == account => wrapperUserBalanceBefore == wrapperSenderBalanceBefore
                && wrapperUserBalanceAfter == wrapperSenderBalanceAfter
                && wrapperUserBalanceBefore == wrapperUserBalanceAfter - value, "wrapper balances wrong update";
    assert e.msg.sender != account => wrapperUserBalanceBefore == wrapperUserBalanceAfter - value
                && wrapperSenderBalanceBefore == wrapperSenderBalanceAfter, "wrapper balances wrong update";
}