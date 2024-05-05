pragma solidity 0.8.0;

contract SimplifiedDeflationaryToken {mapping(address => uint256) public balances;
mapping(address => bool) public isExcludedFromFee;
uint256 public totalSupply = 1000000 * (10**18);
uint256 public transactionFeePercent = 10;
address public owner;

function transfer(address,uint256) public returns(bool) {}
function calculateFee(uint256) public returns(uint256) {}

rule FeeDeductionOnNonExclusion(){
    address $sender;
    address $to;
    uint256 $amount;
    __assume__(msg.sender == $sender);
    uint256 balanceBefore = balances[$sender];
    uint256 balanceBeforeOwner = balances[owner];
    uint256 fee = calculateFee($amount);
    if (!isExcludedFromFee[$sender]){
        transfer($to, $amount);

        // Calculating expected balances after transfer considering the fee
        uint256 expectedSenderBalance = balanceBefore - $amount;
        uint256 expectedOwnerBalance = balanceBeforeOwner + fee;

        // Asserting both sender and owner's balance after transfer
        assert(balances[$sender] == expectedSenderBalance);
        assert(balances[owner] == expectedOwnerBalance);
    }
}}