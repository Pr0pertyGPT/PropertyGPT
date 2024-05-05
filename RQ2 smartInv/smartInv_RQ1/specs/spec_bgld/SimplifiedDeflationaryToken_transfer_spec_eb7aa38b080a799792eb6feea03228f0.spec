pragma solidity 0.8.0;

contract SimplifiedDeflationaryToken {mapping(address => uint256) public balances;
mapping(address => bool) public isExcludedFromFee;
uint256 public totalSupply = 1000000 * (10**18);
uint256 public transactionFeePercent = 10;
address public owner;

function transfer(address,uint256) public returns(bool) {}

rule AssumesRoleBeforeTransfer() {
    address $from;
    address $to;
    uint256 $amount;
    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);
    uint256 balanceBefore = balances[$from];
    uint256 balanceToBefore = balances[$to];
    transfer($to, $amount);
    assert(balances[$from] <= balanceBefore - $amount);
    assert(balances[$to] == balanceToBefore + $amount);
}}