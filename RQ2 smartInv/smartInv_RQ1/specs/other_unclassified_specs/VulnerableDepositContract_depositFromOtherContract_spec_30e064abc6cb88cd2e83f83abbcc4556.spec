pragma solidity 0.8.0;

contract VulnerableDepositContract {mapping(address => uint256) public deposits;

function depositFromOtherContract(uint256,address) public  {}

rule DepositIncreasesAccountBalance() {
    address $forAddress;
    uint256 $depositAmount;
    uint256 balanceBefore = deposits[$forAddress];
    depositFromOtherContract($depositAmount, $forAddress);

    assert((balanceBefore + $depositAmount) == deposits[$forAddress]);
}}