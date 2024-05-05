pragma solidity 0.8.0;

contract SimpleStakeMigration {mapping(address => uint256) public balances;
mapping(address => uint256) public oldBalances;

function migrateStake(address,uint256) public  {}

rule BalanceAfterStakeMigration() {
    address $oldStaking;
    uint256 $amount;
    uint256 oldBalanceBefore = oldBalances[$oldStaking];
    uint256 msgSenderBalanceBefore = balances[msg.sender];

    migrateStake($oldStaking, $amount);

    assert(oldBalanceBefore == oldBalances[$oldStaking] + $amount);
    assert(msgSenderBalanceBefore + $amount == balances[msg.sender]);
}}