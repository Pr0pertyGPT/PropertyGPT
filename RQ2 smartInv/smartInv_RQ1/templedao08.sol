// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStakeMigration {
    mapping(address => uint256) public balances;

    mapping(address => uint256) public oldBalances;

    function migrateStake(address oldStaking, uint256 amount) external {
        require(oldBalances[oldStaking] >= amount, "Insufficient balance in old staking contract");
        
        oldBalances[oldStaking] -= amount;
        
        balances[msg.sender] += amount;
    }
    
    function simulateOldStake(address staker, uint256 amount) external {
        oldBalances[staker] += amount;
    }
}
