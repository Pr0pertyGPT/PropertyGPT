pragma solidity 0.8.0;

contract SimplifiedDeflationaryToken {mapping(address => uint256) public balances;
mapping(address => bool) public isExcludedFromFee;
uint256 public totalSupply = 1000000 * (10**18);
uint256 public transactionFeePercent = 10;
address public owner;

function transfer(address,uint256) public returns(bool) {}
function calculateFee(uint256) public returns(uint256) {}

rule TransferValidBalanceReduction() {
    address $sender;
    uint256 $init_balance;
    balances[$sender] = $init_balance;
    uint256 $amount;
    uint256 fee = calculateFee($amount);
    
    __assume__(msg.sender == $sender);

    if (!isExcludedFromFee[$sender]) {
        transfer($sender, $amount);
        assert(balances[$sender] == $init_balance - $amount - fee);
    } else {
        transfer($sender, $amount);
        assert(balances[$sender] == $init_balance - $amount);
    }
}}