pragma solidity 0.5.17;

contract VulnerableBatchTransfer {mapping(address => uint256) public balances;

function batchTransfer(address[],uint256) public returns(bool) {}

rule BatchTransferMaintainsTotalBalance() {
    address[] $receivers;
    uint256 $value;
    uint256 totalSupplyBefore = totalSupply();

    // Assume different sender scenarios to ensure access control is respected
    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);

    uint256 $senderBalanceBefore = balances[msg.sender];
    uint256 totalSent = $receivers.length * $value;

    batchTransfer($receivers, $value);

    uint256 totalSupplyAfter = totalSupply();
    assert(totalSupplyBefore == totalSupplyAfter); // Ensure total supply is unchanged
    assert(balances[msg.sender] == $senderBalanceBefore - totalSent); // Ensure sender's balance decreases correctly
}}