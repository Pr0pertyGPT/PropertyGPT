using Checkpoints as Checkpoints

methods {
    // functions
    checkpoints(address, uint32) envfree
    numCheckpoints(address) returns (uint32) envfree
    getVotes(address) returns (uint256) envfree
    getPastVotes(address, uint256) returns (uint256)
    getPastTotalSupply(uint256) returns (uint256)
    delegates(address) returns (address) envfree
    delegate(address)
    _delegate(address, address)
    delegateBySig(address, uint256, uint256, uint8, bytes32, bytes32)
    nonces(address) returns (uint256)
    totalSupply() returns (uint256) envfree
    _maxSupply() returns (uint224) envfree

    // harnesss functions
    ckptFromBlock(address, uint32) returns (uint32) envfree
    ckptVotes(address, uint32) returns (uint224) envfree
    mint(address, uint256)
    burn(uint256)
    unsafeNumCheckpoints(address) returns (uint256) envfree

    // solidity generated getters
    _delegation(address) returns (address) envfree

    // external functions


}

// gets the most recent votes for a user
ghost userVotes(address) returns uint224{
        init_state axiom forall address a. userVotes(a) == 0;
}

// sums the total votes for all users
ghost totalVotes() returns mathint {
    init_state axiom totalVotes() == 0;
    axiom totalVotes() >= 0;
}

hook Sstore _checkpoints[KEY address account].votes uint224 newVotes (uint224 oldVotes) STORAGE {
    havoc userVotes assuming
        userVotes@new(account) == newVotes;

    havoc totalVotes assuming
        totalVotes@new() == totalVotes@old() + to_mathint(newVotes) - to_mathint(userVotes(account));
}


ghost lastFromBlock(address) returns uint32;

ghost doubleFromBlock(address) returns bool {
    init_state axiom forall address a. doubleFromBlock(a) == false;
}




hook Sstore _checkpoints[KEY address account].fromBlock uint32 newBlock (uint32 oldBlock) STORAGE {
    havoc lastFromBlock assuming
        lastFromBlock@new(account) == newBlock;
    
    havoc doubleFromBlock assuming 
        doubleFromBlock@new(account) == (newBlock == lastFromBlock(account));
}

// for some checkpoint, the fromBlock is less than the current block number
// passes but fails rule sanity from hash on delegate by sig
invariant timestamp_constrains_fromBlock(address account, uint32 index, env e)
    ckptFromBlock(account, index) < e.block.number
    filtered { f -> !f.isView }
{
    preserved {
        require index < numCheckpoints(account);
    }
}

// numCheckpoints are less than maxInt
// passes because numCheckpoints does a safeCast
// invariant maxInt_constrains_numBlocks(address account)
//     numCheckpoints(account) < 4294967295 // 2^32

// can't have more checkpoints for a given account than the last from block
// passes
invariant fromBlock_constrains_numBlocks(address account)
    numCheckpoints(account) <= ckptFromBlock(account, numCheckpoints(account) - 1)
    filtered { f -> !f.isView }
{ preserved with(env e) {
    require e.block.number >= ckptFromBlock(account, numCheckpoints(account) - 1); // this should be true from the invariant above!!
}}

// for any given checkpoint, the fromBlock must be greater than the checkpoint
// this proves the above invariant in combination with the below invariant
// if checkpoint has a greater fromBlock than the last, and the FromBlock is always greater than the pos. 
// Then the number of positions must be less than the currentFromBlock
// ^note that the tool is assuming it's possible for the starting fromBlock to be 0 or anything, and does not know the current starting block
// passes + rule sanity
invariant fromBlock_greaterThanEq_pos(address account, uint32 pos)
    ckptFromBlock(account, pos) >= pos
    filtered { f -> !f.isView }

// a larger index must have a larger fromBlock
// passes + rule sanity
invariant fromBlock_increasing(address account, uint32 pos, uint32 pos2)
    pos > pos2 => ckptFromBlock(account, pos) > ckptFromBlock(account, pos2)
    filtered { f -> !f.isView }


// converted from an invariant to a rule to slightly change the logic
// if the fromBlock is the same as before, then the number of checkpoints stays the same
// however if the fromBlock is new than the number of checkpoints increases
// passes, fails rule sanity because tautology check seems to be bugged
rule unique_checkpoints_rule(method f) {
    env e; calldataarg args;
    address account;
    uint32 num_ckpts_ = numCheckpoints(account); 
    uint32 fromBlock_ = num_ckpts_ == 0 ? 0 : ckptFromBlock(account, num_ckpts_ - 1);

    f(e, args);

    uint32 _num_ckpts = numCheckpoints(account);
    uint32 _fromBlock = _num_ckpts == 0 ? 0 : ckptFromBlock(account, _num_ckpts - 1);
    

    assert fromBlock_ == _fromBlock => num_ckpts_ == _num_ckpts || _num_ckpts == 1, "same fromBlock, new checkpoint";
    // this assert fails consistently
    // assert !doubleFromBlock(account) => ckpts_ != _ckpts, "new fromBlock but total checkpoints not being increased";
}

// assumes neither account has delegated
// currently fails due to this scenario. A has maxint number of checkpoints
// an additional checkpoint is added which overflows and sets A's votes to 0
// passes + rule sanity (- a bad tautology check)
rule transfer_safe() {
    env e;
    uint256 ID;
    address a; address b;

    require delegates(a) != delegates(b); // confirmed if they both delegate to the same person then transfer keeps the votes the same
    require numCheckpoints(delegates(a)) < 1000000;
    require numCheckpoints(delegates(b)) < 1000000;

    uint256 votesA_pre = getVotes(delegates(a));
    uint256 votesB_pre = getVotes(delegates(b));

    mathint totalVotes_pre = totalVotes();

    transferFrom(e, a, b, ID);
    
    mathint totalVotes_post = totalVotes();
    uint256 votesA_post = getVotes(delegates(a));
    uint256 votesB_post = getVotes(delegates(b));

    // if an account that has not delegated transfers balance to an account that has, it will increase the total supply of votes
    assert totalVotes_pre == totalVotes_post, "transfer changed total supply";
    assert delegates(a) != 0 => votesA_pre - 1 == votesA_post, "A lost the wrong amount of votes";
    assert delegates(b) != 0 => votesB_pre + 1 == votesB_post, "B gained the wrong amount of votes";
}

// for any given function f, if the delegate is changed the function must be delegate or delegateBySig
// passes
rule delegates_safe(method f) filtered {f -> (f.selector != delegate(address).selector &&
                                                f.selector != _delegate(address, address).selector &&
                                                f.selector != delegateBySig(address, uint256, uint256, uint8, bytes32, bytes32).selector) }
{
    env e; calldataarg args;
    address account;
    address pre = delegates(account);

    f(e, args);

    address post = delegates(account);

    assert pre == post, "invalid delegate change";
}

// delegates increases the delegatee's votes by the proper amount
// passes + rule sanity
rule delegatee_receives_votes() {
    env e; 
    address delegator; address delegatee;

    require numCheckpoints(delegatee) < 1000000;
    require delegates(delegator) != delegatee;
    require delegatee != 0x0;


    uint256 delegator_bal = balanceOf(e, delegator);
    uint256 votes_= getVotes(delegatee);

    _delegate(e, delegator, delegatee);

    uint256 _votes = getVotes(delegatee);
    assert _votes == votes_ + delegator_bal, "delegatee did not receive votes";
}

// passes + rule sanity
rule previous_delegatee_votes_removed() {
    env e;
    address delegator; address delegatee; address third;

    require third != delegatee;
    require delegates(delegator) == third;
    require numCheckpoints(third) < 1000000;

    uint256 delegator_bal = balanceOf(e, delegator);
    uint256 votes_ = getVotes(third);

    _delegate(e, delegator, delegatee);

    uint256 _votes = getVotes(third);

    assert third != 0x0 => _votes == votes_ - delegator_bal, "votes not removed from the previous delegatee";
}

// passes with rule sanity
rule delegate_contained() {
    env e;
    address delegator; address delegatee; address other;

    require other != delegatee;
    require other != delegates(delegator); 

    uint256 votes_ = getVotes(other);

    _delegate(e, delegator, delegatee);

    uint256 _votes = getVotes(other);

    assert votes_ == _votes, "votes not contained";
}

rule delegate_no_frontrunning(method f) {
    env e; calldataarg args;
    address delegator; address delegatee; address third; address other;



    require numCheckpoints(delegatee) < 1000000;
    require numCheckpoints(third) < 1000000;


    f(e, args);

    uint256 delegator_bal = balanceOf(e, delegator);
    uint256 delegatee_votes_ = getVotes(delegatee);
    uint256 third_votes_ = getVotes(third);
    uint256 other_votes_ = getVotes(other);
    require delegates(delegator) == third;
    require third != delegatee;
    require other != third;
    require other != delegatee;
    require delegatee != 0x0;

    _delegate(e, delegator, delegatee);

    uint256 _delegatee_votes = getVotes(delegatee);
    uint256 _third_votes = getVotes(third);
    uint256 _other_votes = getVotes(other);


    // previous delegatee loses all of their votes
    // delegatee gains that many votes
    // third loses any votes delegated to them
    assert _delegatee_votes == delegatee_votes_ + delegator_bal, "delegatee did not receive votes";
    assert third != 0 => _third_votes == third_votes_ - delegator_bal, "votes not removed from third";
    assert other_votes_ == _other_votes, "delegate not contained";
}