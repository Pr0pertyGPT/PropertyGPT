pragma solidity 0.5.17;

contract VulnerableBatchTransfer {mapping(address => uint256) public balances;

function transfer(address,uint256) public returns(bool) {}

rule EnsureProperTransferEffect() {
    address $senderInitial;
    address $receiverInitial;
    uint256 $senderBalance;
    uint256 $receiverBalance;
    uint256 $transferAmount;

    // Assuming initial state for balances
    balances[$senderInitial] = $senderBalance;
    balances[$receiverInitial] = $receiverBalance;
    
    __assume__(msg.sender == $senderInitial);
    
    // Simulating transfer conditions
    require($transferAmount <= $senderBalance, "Transfer amount exceeds sender balance");
    require($receiverInitial != address(0), "Cannot transfer to the zero address");

    uint256 senderBalanceBefore = balances[msg.sender];
    uint256 receiverBalanceBefore = balances[$receiverInitial];
    
    transfer($receiverInitial, $transferAmount);
    
    assert(balances[msg.sender] == senderBalanceBefore - $transferAmount);
    assert(balances[$receiverInitial] == receiverBalanceBefore + $transferAmount);
}}