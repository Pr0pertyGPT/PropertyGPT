pragma solidity 0.8.0;

contract SimpleStakeMigration {mapping(address => uint256) public balances;
mapping(address => uint256) public oldBalances;

function migrateStake(address,uint256) public  {}

rule MigrateStakeBalanceTransfer() {
    address $oldStaking;
    uint256 $amount;
    address $sender = msg.sender;
    uint256 initOldBalance = oldBalances[$oldStaking];
    uint256 initSenderBalance = balances[$sender];
    
    migrateStake($oldStaking, $amount);
    
    assert(oldBalances[$oldStaking] == initOldBalance - $amount);
    assert(balances[$sender] == initSenderBalance + $amount);
}}