pragma solidity 0.8.0;

contract VulnerableDepositContract {mapping(address => uint256) public deposits;

function depositFromOtherContract(uint256,address) public  {}

rule depositFromOtherContractMaintainsTotalDeposited() {
    address $forAddress;
    uint256 $depositAmount;

    // Initial stored deposit for the address
    uint256 depositForAddressBefore = deposits[$forAddress];
    
    // Perform the deposit from another contract
    depositFromOtherContract($depositAmount, $forAddress);
    
    // Assert the deposit amount has correctly been added to the address's deposit
    assert(deposits[$forAddress] == depositForAddressBefore + $depositAmount);
}}