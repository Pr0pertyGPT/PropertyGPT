pragma solidity 0.8.0;

contract VulnerableDepositContract {mapping(address => uint256) public deposits;

function depositFromOtherContract(uint256,address) public  {}

rule depositIncreasesAccountBalanceCorrectly() {
    address $depositor;
    uint256 $init_deposit_amount;
    address $forAddress;
    uint256 balanceBefore = deposits[$forAddress];
    uint256 $depositAmount;

    depositFromOtherContract($depositAmount, $forAddress);

    assert(deposits[$forAddress] == (balanceBefore + $depositAmount));
}}