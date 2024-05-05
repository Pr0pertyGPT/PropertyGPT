pragma solidity 0.8.0;

contract VulnerableStaking {mapping(address => uint256) public balances;
uint256 public totalSupply;


rule ensureDepositReflectsInBalancesAndTotalSupply() {
    address $sender;
    uint256 $init_balance_sender;
    uint256 $init_totalSupply;
    uint256 $amount;

    balances[$sender] = $init_balance_sender;
    totalSupply = $init_totalSupply;

    // emulate the deposit by directly modifying balances and totalSupply
    balances[$sender] += $amount;
    totalSupply += $amount;

    assert(balances[$sender] == $init_balance_sender + $amount);
    assert(totalSupply == $init_totalSupply + $amount);
}}