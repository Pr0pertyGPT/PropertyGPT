pragma solidity 0.8.0;

contract SimplifiedDeflationaryToken {mapping(address => uint256) public balances;
mapping(address => bool) public isExcludedFromFee;
uint256 public totalSupply = 1000000 * (10**18);
uint256 public transactionFeePercent = 10;
address public owner;

function transfer(address,uint256) public returns(bool) {}
function calculateFee(uint256) public returns(uint256) {}

rule TransferUpdatesBalancesCorrectly() {
    address $sender; // symbolize the sender
    address $to; // symbolize the receiver
    uint256 $amount;
    uint256 init_sender_balance = balances[$sender];
    uint256 init_to_balance = balances[$to];
    uint256 init_owner_balance = balances[owner];
    
    __assume__(msg.sender == $sender); // Assume control over msg.sender
    transfer($to, $amount);

    uint256 fee = isExcludedFromFee[$sender] ? 0 : calculateFee($amount);
    assert(balances[$sender] == init_sender_balance - $amount); // sender balance is deducted by amount
    assert(balances[$to] == init_to_balance + $amount - fee); // recipient balance is increased by amount minus fee
    assert(balances[owner] == init_owner_balance + fee); // owner balance is increased by fee
}}