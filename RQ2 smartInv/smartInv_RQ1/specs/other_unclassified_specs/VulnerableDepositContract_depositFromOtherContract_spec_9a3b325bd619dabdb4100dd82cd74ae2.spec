pragma solidity 0.8.0;

contract VulnerableDepositContract {mapping(address => uint256) public deposits;

function depositFromOtherContract(uint256,address) public  {}

rule PreserveBalanceAfterDeposit() {
    address $depositAddress;
    uint256 $depositAmount;
    uint256 balanceBefore = deposits[$depositAddress];
    depositFromOtherContract($depositAmount, $depositAddress);

    assert(deposits[$depositAddress] == balanceBefore + $depositAmount);
}}