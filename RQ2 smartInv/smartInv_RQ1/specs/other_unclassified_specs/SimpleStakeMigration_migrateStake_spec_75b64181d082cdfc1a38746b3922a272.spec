pragma solidity 0.8.0;

contract SimpleStakeMigration {mapping(address => uint256) public balances;
mapping(address => uint256) public oldBalances;

function migrateStake(address,uint256) public  {}

rule MigrationDecreasesOldAndIncreasesNewBalances() {
        address $oldStaking;
        uint256 $amount;
        uint256 oldBalanceBefore = oldBalances[$oldStaking];
        uint256 newBalanceBefore = balances[msg.sender];
        
        migrateStake($oldStaking, $amount);
        
        assert(oldBalances[$oldStaking] == oldBalanceBefore - $amount);
        assert(balances[msg.sender] == newBalanceBefore + $amount);
    }}