pragma solidity 0.8.0;

contract SimplifiedDeflationaryToken {mapping(address => uint256) public balances;
mapping(address => bool) public isExcludedFromFee;
uint256 public totalSupply = 1000000 * (10**18);
uint256 public transactionFeePercent = 10;
address public owner;

function transfer(address,uint256) public returns(bool) {}
function calculateFee(uint256) public returns(uint256) {}

rule TransferFeeCorrectness() {
    address $sender;
    address $to;
    uint256 $amount;
    uint256 $init_sender_balance = balances[$sender];
    uint256 $init_to_balance = balances[$to];
    uint256 $init_owner_balance = balances[owner];
    __assume__(msg.sender == $sender);

    transfer($to, $amount);

    uint256 $fee = 0;
    if (!isExcludedFromFee[$sender]) {
        $fee = calculateFee($amount);
    }
    assert(balances[$sender] == $init_sender_balance - $amount);
    assert(balances[$to] == $init_to_balance + ($amount - $fee));
    assert(balances[owner] == $init_owner_balance + $fee);
}}