pragma solidity 0.8.0;

contract SimpleStakeMigration{mapping(address => uint256) public balances;
mapping(address => uint256) public oldBalances;
function migrateStake(address,uint256) public   
precondition{oldBalances[oldStaking] >= amount}

postcondition{oldBalances[oldStaking] == __old__(oldBalances[oldStaking]) - amount; balances[msg.sender] == __old__(balances[msg.sender]) + amount}
}