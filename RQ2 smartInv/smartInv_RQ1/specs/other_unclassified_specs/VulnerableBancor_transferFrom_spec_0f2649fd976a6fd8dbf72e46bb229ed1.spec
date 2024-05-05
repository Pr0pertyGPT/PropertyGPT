pragma solidity 0.8.0;

contract VulnerableBancor {mapping(address => mapping(address => uint256)) public allowance;
mapping(address => uint256) public balanceOf;

function transferFrom(address,address,uint256) public returns(bool) {}

rule TransferFromCorrectnessCheck() {
    address $from;
    address $to;
    uint256 $value;

    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);
    __assume__(balanceOf[$from] >= $value);
    __assume__(allowance[$from][msg.sender] >= $value);

    uint256 initial_balance_from = balanceOf[$from];
    uint256 initial_balance_to = balanceOf[$to];
    uint256 initial_allowance = allowance[$from][msg.sender];

    transferFrom($from, $to, $value);

    assert(balanceOf[$from] == initial_balance_from - $value);
    assert(balanceOf[$to] == initial_balance_to + $value);
    assert(allowance[$from][msg.sender] == initial_allowance - $value);
}}