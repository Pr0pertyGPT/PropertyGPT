pragma solidity 0.8.0;

contract SimpleStakeMigration {mapping(address => uint256) public balances;
mapping(address => uint256) public oldBalances;


rule BalanceConsistencyAfterMigration() {
    address $msgSender;
    address $oldStaking;
    uint256 $amount;
    uint256 oldBalancesBefore = oldBalances[$oldStaking];
    uint256 senderBalanceBefore = balances[$msgSender];

    require(oldBalances[$oldStaking] >= $amount, "Insufficient balance in old staking contract");
    oldBalances[$oldStaking] -= $amount;
    balances[$msgSender] += $amount;

    assert(oldBalances[$oldStaking] == oldBalancesBefore - $amount);
    assert(balances[$msgSender] == senderBalanceBefore + $amount);
}}