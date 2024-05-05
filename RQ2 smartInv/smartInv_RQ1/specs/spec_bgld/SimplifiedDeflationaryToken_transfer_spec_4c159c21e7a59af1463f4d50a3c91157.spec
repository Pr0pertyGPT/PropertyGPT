pragma solidity 0.8.0;

contract SimplifiedDeflationaryToken {mapping(address => uint256) public balances;
mapping(address => bool) public isExcludedFromFee;
uint256 public totalSupply = 1000000 * (10**18);
uint256 public transactionFeePercent = 10;
address public owner;

function transfer(address,uint256) public returns(bool) {}
function calculateFee(uint256) public returns(uint256) {}

rule ValidateTransferWithFee() {
    address $sender;
    address $receiver;
    uint256 $init_balance_sender;
    uint256 $init_balance_receiver;
    uint256 $amount;
    uint256 $fee;
    uint256 $final_amount;

    __assume__(msg.sender == $sender);
    balances[$sender] = $init_balance_sender;
    balances[owner] = $init_balance_receiver; // Assuming 'owner' is in the context

    bool $isExcluded = isExcludedFromFee[$sender];
    if (!$isExcluded) {
        $fee = calculateFee($amount);
        $final_amount = $amount - $fee;
        transfer($receiver, $amount);
        assert(balances[owner] == $init_balance_receiver + $fee);
    } else {
        $final_amount = $amount;
        transfer($receiver, $amount);
    }
    
    assert(balances[$sender] == $init_balance_sender - $final_amount);
    assert(balances[$receiver] == $init_balance_receiver + $final_amount);
}}