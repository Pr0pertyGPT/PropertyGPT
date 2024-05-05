pragma solidity 0.8.0;

contract SimplifiedDeflationaryToken {mapping(address => uint256) public balances;
mapping(address => bool) public isExcludedFromFee;
uint256 public totalSupply = 1000000 * (10**18);
uint256 public transactionFeePercent = 10;
address public owner;

function transfer(address,uint256) public returns(bool) {}

rule SenderBalanceNotDecreasedImproperly() {
    address $sender;
    address $to;
    uint256 $initialSenderBalance = balances[$sender];
    uint256 $amount;

    // Assuming the sender has enough balance
    __assume__(balances[$sender] >= $amount);

    // Making the actual transfer
    transfer($to, $amount);

    // Checking if the sender's balance is properly decreased
    assert(balances[$sender] == $initialSenderBalance - $amount);
}}