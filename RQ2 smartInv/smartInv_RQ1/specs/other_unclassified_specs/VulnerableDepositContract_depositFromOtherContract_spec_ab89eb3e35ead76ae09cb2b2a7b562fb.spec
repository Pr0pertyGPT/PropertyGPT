pragma solidity 0.8.0;

contract VulnerableDepositContract {mapping(address => uint256) public deposits;

function depositFromOtherContract(uint256,address) public  {}

rule CorrectDepositFromOtherContract() {
    address $depositor;
    address $beneficiary;
    uint256 $depositAmount;
    uint256 init_balance = deposits[$beneficiary];
    
    depositFromOtherContract($depositAmount, $beneficiary);

    if ($depositor != $beneficiary) {
        assert((init_balance + $depositAmount) == deposits[$beneficiary]);
    } else {
        assert(init_balance == deposits[$beneficiary]);
    }
}}