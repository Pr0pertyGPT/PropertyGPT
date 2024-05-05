pragma solidity 0.8.0;

contract VulnerableDepositContract {mapping(address => uint256) public deposits;

function depositFromOtherContract(uint256,address) public  {}

rule DepositIncreasesAccountBalanceCorrectly() {
    address $depositor;
    uint256 $depositAmount;
    address $forAddress;
    
    uint256 depositedBefore = deposits[$forAddress];
    depositFromOtherContract($depositAmount, $forAddress);
    uint256 depositedAfter = deposits[$forAddress];
    
    assert(depositedAfter == depositedBefore + $depositAmount);
}}