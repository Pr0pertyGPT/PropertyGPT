pragma solidity 0.8.0;

contract VulnerableDepositContract {mapping(address => uint256) public deposits;

function depositFromOtherContract(uint256,address) public  {}

rule DepositIncreasesAccountBalance() {
    address $depositor;
    uint256 $depositAmount;
    uint256 initBalance = deposits[$depositor];
    depositFromOtherContract($depositAmount, $depositor);

    assert(deposits[$depositor] == initBalance + $depositAmount);
}}