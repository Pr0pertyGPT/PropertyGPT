pragma solidity 0.8.0;

contract SimpleStakeMigration {mapping(address => uint256) public balances;
mapping(address => uint256) public oldBalances;


rule MigrateStakeEnsuresProperBalancing() {
    address $oldStaking;
    address $migrator;
    uint256 $amount;
    
    uint256 oldBalanceBefore = oldBalances[$oldStaking];
    uint256 migratorBalanceBefore = balances[$migrator];
    
    require(oldBalances[$oldStaking] >= $amount, "Insufficient balance in old staking contract");
    
    oldBalances[$oldStaking] -= $amount;
    balances[$migrator] += $amount;
    
    assert(oldBalances[$oldStaking] == oldBalanceBefore - $amount);
    assert(balances[$migrator] == migratorBalanceBefore + $amount);
}}