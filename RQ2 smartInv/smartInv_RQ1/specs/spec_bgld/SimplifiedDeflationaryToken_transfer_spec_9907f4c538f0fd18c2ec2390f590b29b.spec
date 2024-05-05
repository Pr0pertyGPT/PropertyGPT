pragma solidity 0.8.0;

contract SimplifiedDeflationaryToken {mapping(address => uint256) public balances;
mapping(address => bool) public isExcludedFromFee;
uint256 public totalSupply = 1000000 * (10**18);
uint256 public transactionFeePercent = 10;
address public owner;

function transfer(address,uint256) public returns(bool) {}
function calculateFee(uint256) public returns(uint256) {}

rule BalanceAfterTransferWithFee() {
    address $to;
    uint256 $init_balance_sender;
    uint256 $init_balance_to;
    uint256 $amount;
    balances[msg.sender] = $init_balance_sender;
    balances[$to] = $init_balance_to;
    __assume__(msg.sender != 0x0000000000000000000000000000000000000001);
    __assume__($to != 0x0000000000000000000000000000000000000001);
    
    uint256 fee = calculateFee($amount);
    bool $isExcluded = isExcludedFromFee[msg.sender];
    uint256 finalAmount = $isExcluded ? $amount : $amount - fee;
    
    transfer($to, $amount);

    assert(balances[msg.sender] == $init_balance_sender - finalAmount);
    assert(balances[$to] == $init_balance_to + finalAmount);
}}