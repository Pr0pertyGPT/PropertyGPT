pragma solidity 0.5.17;

contract VulnerableBatchTransfer {mapping(address => uint256) public balances;

function transfer(address,uint256) public returns(bool) {}

rule TransferChecksBalanceDecrease() {
    address $sender = msg.sender;
    uint256 $init_sender_balance = balances[$sender];
    uint256 $amount;
    address $receiver;

    __assume__($receiver != address(0));
    __assume__($init_sender_balance >= $amount);

    uint256 balanceBeforeSender = balances[$sender];
    uint256 balanceBeforeReceiver = balances[$receiver];
    transfer($receiver, $amount);
    assert((balanceBeforeSender - $amount) == balances[$sender]);
    assert((balanceBeforeReceiver + $amount) == balances[$receiver]);
}}