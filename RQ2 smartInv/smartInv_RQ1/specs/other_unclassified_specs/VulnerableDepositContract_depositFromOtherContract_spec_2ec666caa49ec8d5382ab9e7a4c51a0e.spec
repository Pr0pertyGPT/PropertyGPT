pragma solidity 0.8.0;

contract VulnerableDepositContract {mapping(address => uint256) public deposits;

function depositFromOtherContract(uint256,address) public  {}

rule CheckDepositIntegrity() {
    address $_forAddress;
    uint256 $_depositAmount;

    uint256 balanceBefore = deposits[$_forAddress];
    depositFromOtherContract($_depositAmount, $_forAddress);

    assert(deposits[$_forAddress] == balanceBefore + $_depositAmount);
}}