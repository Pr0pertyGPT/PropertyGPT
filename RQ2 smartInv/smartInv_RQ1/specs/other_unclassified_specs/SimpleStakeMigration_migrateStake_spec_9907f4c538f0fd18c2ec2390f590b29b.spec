pragma solidity 0.8.0;

contract SimpleStakeMigration {mapping(address => uint256) public balances;
mapping(address => uint256) public oldBalances;

function migrateStake(address,uint256) public  {}

rule MigrateStakeEffectsOnBalances() {
    address $oldStaking;
    uint256 $amount;
    address $sender = msg.sender;
    
    uint256 balance_oldStaking_before = oldBalances[$oldStaking];
    uint256 balance_sender_before = balances[$sender];
    
    migrateStake($oldStaking, $amount);

    assert(oldBalances[$oldStaking] == balance_oldStaking_before - $amount);
    assert(balances[$sender] == balance_sender_before + $amount);
}}