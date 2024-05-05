pragma solidity 0.5.17;

contract VulnerableBatchTransfer {mapping(address => uint256) public balances;

function transfer(address,uint256) public returns(bool) {}

rule SenderHasSufficientBalance() {
    address $sender;
    uint256 $init_balance_sender;
    balances[$sender] = $init_balance_sender;
    address $receiver;
    uint256 $transfer_amount;
    
    __assume__(msg.sender == $sender);
    
    // Simulate condition where sender does not have sufficient balance
    require($init_balance_sender < $transfer_amount);
    
    bool success = transfer($receiver, $transfer_amount);
    assert(!success);
}}