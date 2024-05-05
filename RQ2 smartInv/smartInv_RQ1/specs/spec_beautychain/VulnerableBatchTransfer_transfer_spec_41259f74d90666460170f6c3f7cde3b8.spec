pragma solidity 0.5.17;

contract VulnerableBatchTransfer {mapping(address => uint256) public balances;

function transfer(address,uint256) public returns(bool) {}

rule EnsureTransferFromSenderDecreasesBalance() {
    address $sender;
    address $receiver;
    uint256 $init_sender_balance;
    uint256 $value;
    __assume__(msg.sender == $sender);

    balances[msg.sender] = $init_sender_balance;
    require($init_sender_balance >= $value, "Initial balance must be sufficient for transfer");

    uint256 balanceBefore = balances[msg.sender];
    transfer($receiver, $value);
    // Checking if sender's balance decreased by the amount transferred.
    assert(balanceBefore - $value == balances[msg.sender]);
}}