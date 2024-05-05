pragma solidity 0.8.0;

contract VulnerableDepositContract {mapping(address => uint256) public deposits;

function depositFromOtherContract(uint256,address) public  {}

rule VerifyDepositFromOtherContractIncreasesBalance() {
        address $depositor;
        address $beneficiary;
        uint256 $depositAmount;
        
        uint256 balanceBefore = deposits[$beneficiary];
        depositFromOtherContract($depositAmount, $beneficiary);
        
        assert(deposits[$beneficiary] == balanceBefore + $depositAmount);
    }}