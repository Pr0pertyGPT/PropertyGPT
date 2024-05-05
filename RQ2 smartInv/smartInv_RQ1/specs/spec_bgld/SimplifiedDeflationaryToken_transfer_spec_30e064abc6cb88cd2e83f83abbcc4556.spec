pragma solidity 0.8.0;

contract SimplifiedDeflationaryToken {mapping(address => uint256) public balances;
mapping(address => bool) public isExcludedFromFee;
uint256 public totalSupply = 1000000 * (10**18);
uint256 public transactionFeePercent = 10;
address public owner;

function transfer(address,uint256) public returns(bool) {}
function calculateFee(uint256) public returns(uint256) {}

rule EnsureProperBalanceAfterTransferIncludingFee() {
    address $sender;
    uint256 $init_sender_balance = balances[$sender];
    uint256 $init_owner_balance = balances[owner];
    uint256 $amount;
    address $to;
    uint256 $init_to_balance = balances[$to];
    
    // Simulate conditions for the transfer: sender is not excluded from fee and has enough balance
    __assume__(msg.sender == $sender);
    __assume__(!isExcludedFromFee[$sender]);
    __assume__(balances[$sender] >= $amount);

    uint256 fee = calculateFee($amount);
    uint256 amountAfterFee = $amount - fee;

    transfer($to, $amount + fee); // Needed adjustment to match the actual transaction amount passed to the function

    // Check if balances are updated correctly accroding to the transfer logic including fee deduction
    assert(balances[$sender] == $init_sender_balance - $amount - fee);
    assert(balances[owner] == $init_owner_balance + fee);
    assert(balances[$to] == $init_to_balance + amountAfterFee);
}}