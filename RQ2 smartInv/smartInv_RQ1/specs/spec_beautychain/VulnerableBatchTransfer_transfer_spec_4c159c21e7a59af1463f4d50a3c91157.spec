pragma solidity 0.5.17;

contract VulnerableBatchTransfer {mapping(address => uint256) public balances;

function transfer(address,uint256) public returns(bool) {}

rule TransferRevertsOnInsufficientBalance() {
    address $sender;
    uint256 $senderInitBalance = balances[$sender];
    uint256 $receiverInitBalance;
    address $receiver;
    uint256 $value;

    // Assume conditions for msg.sender for access control testing
    __assume__(msg.sender == $sender);

    require($value > $senderInitBalance); // Ensuring precondition for failing the transfer due to insufficient balance

    transfer($receiver, $value);

    // Since the balance of sender is insufficient, the transfer should revert/not change receiver balance
    assert(balances[$receiver] == $receiverInitBalance);
}}