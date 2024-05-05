pragma solidity 0.8.0;

contract SimpleStakeMigration {mapping(address => uint256) public balances;
mapping(address => uint256) public oldBalances;

function migrateStake(address,uint256) public  {}

rule VerifyStakeMigrationBalances() {
    address $oldStaking;
    uint256 $amount;
    uint256 oldStakeBalanceBefore = oldBalances[$oldStaking];
    uint256 senderBalanceBefore = balances[msg.sender];
    
    migrateStake($oldStaking, $amount);

    assert(oldBalances[$oldStaking] == oldStakeBalanceBefore - $amount);
    assert(balances[msg.sender] == senderBalanceBefore + $amount);
}}