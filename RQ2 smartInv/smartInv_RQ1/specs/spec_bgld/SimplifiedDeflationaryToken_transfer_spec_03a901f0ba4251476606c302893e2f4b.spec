pragma solidity 0.8.0;

contract SimplifiedDeflationaryToken {mapping(address => uint256) public balances;
mapping(address => bool) public isExcludedFromFee;
uint256 public totalSupply = 1000000 * (10**18);
uint256 public transactionFeePercent = 10;
address public owner;

function transfer(address,uint256) public returns(bool) {}
function calculateFee(uint256) public returns(uint256) {}

rule ensureCorrectFeeApplied() {
    address $sender;
    address $to;
    uint256 $initialBalanceSender;
    uint256 $feePercentage; // Assuming there's a function or a state variable to get this
    uint256 $amount;
    bool $isExcluded;

    __assume__(msg.sender == $sender);
    balances[msg.sender] = $initialBalanceSender;
    isExcludedFromFee[msg.sender] = $isExcluded;

    uint256 feeExpected = $isExcluded ? 0 : calculateFee($amount);
    uint256 balanceAfterTransfer = $initialBalanceSender - $amount - feeExpected;
    
    transfer($to, $amount);

    assert(balances[msg.sender] == balanceAfterTransfer);
}}