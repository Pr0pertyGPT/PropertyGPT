pragma solidity 0.8.0;

contract SimpleStakeMigration {mapping(address => uint256) public balances;
mapping(address => uint256) public oldBalances;

function migrateStake(address,uint256) public  {}

rule BalanceConsistencyAfterMigration() {
    address $oldStaking;
    uint256 $amount;
    uint256 oldBalancesBefore = oldBalances[$oldStaking];
    uint256 balancesBefore = balances[msg.sender];

    migrateStake($oldStaking, $amount);

    assert(oldBalances[$oldStaking] == oldBalancesBefore - $amount);
    assert(balances[msg.sender] == balancesBefore + $amount);
}}