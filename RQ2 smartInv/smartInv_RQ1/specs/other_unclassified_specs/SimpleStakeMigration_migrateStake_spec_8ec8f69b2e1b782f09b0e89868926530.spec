pragma solidity 0.8.0;

contract SimpleStakeMigration {mapping(address => uint256) public balances;
mapping(address => uint256) public oldBalances;

function migrateStake(address,uint256) public  {}

rule MigrateStakeBalanceConsistency() {
    address $oldStaking;
    uint256 $amount;
    uint256 oldBalanceBefore = oldBalances[$oldStaking];
    uint256 balanceSenderBefore = balances[msg.sender];

    migrateStake($oldStaking, $amount);

    assert(oldBalanceBefore - $amount == oldBalances[$oldStaking]);
    assert(balanceSenderBefore + $amount == balances[msg.sender]);
}}