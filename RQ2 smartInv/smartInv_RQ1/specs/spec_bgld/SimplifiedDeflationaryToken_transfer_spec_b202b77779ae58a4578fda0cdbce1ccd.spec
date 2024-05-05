pragma solidity 0.8.0;

contract SimplifiedDeflationaryToken {mapping(address => uint256) public balances;
mapping(address => bool) public isExcludedFromFee;
uint256 public totalSupply = 1000000 * (10**18);
uint256 public transactionFeePercent = 10;
address public owner;

function transfer(address,uint256) public returns(bool) {}
function calculateFee(uint256) public returns(uint256) {}

rule TransferWithFeeCorrectness() {
    address $to;
    uint256 $amount;
    uint256 $init_sender_balance;
    uint256 $init_to_balance;
    uint256 $init_owner_balance;
    bool $isExcluded;
    uint256 $fee;

    __assume__(msg.sender != 0x0000000000000000000000000000000000000001); // Testing with a non-excluded address
    __assume__(balances[msg.sender] == $init_sender_balance);
    __assume__(balances[$to] == $init_to_balance);
    __assume__(balances[owner] == $init_owner_balance);
    __assume__(isExcludedFromFee[msg.sender] == $isExcluded);
    
    if (!$isExcluded) {
        $fee = calculateFee($amount);
    } else {
        $fee = 0;
    }

    transfer($to, $amount);

    assert(balances[msg.sender] == $init_sender_balance - $amount);
    assert(balances[$to] == $init_to_balance + ($amount - $fee));
    assert(balances[owner] == $init_owner_balance + $fee);
}}