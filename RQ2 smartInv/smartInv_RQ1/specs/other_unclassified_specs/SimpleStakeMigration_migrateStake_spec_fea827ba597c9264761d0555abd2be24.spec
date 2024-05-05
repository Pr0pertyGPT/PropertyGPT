pragma solidity 0.8.0;

contract SimpleStakeMigration {mapping(address => uint256) public balances;
mapping(address => uint256) public oldBalances;

function migrateStake(address,uint256) public  {}

rule BalanceConsistencyAfterMigration() {
    address $oldStaking;
    uint256 $amount;
    uint256 balanceOldStakingBefore = oldBalances[$oldStaking];
    uint256 balanceSenderBefore = balances[msg.sender];

    migrateStake($oldStaking, $amount);

    assert(oldBalances[$oldStaking] == balanceOldStakingBefore - $amount);
    assert(balances[msg.sender] == balanceSenderBefore + $amount);
}}