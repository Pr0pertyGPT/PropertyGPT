pragma solidity 0.8.0;

contract VulnerableBancor {mapping(address => mapping(address => uint256)) public allowance;
mapping(address => uint256) public balanceOf;

function transferFrom(address,address,uint256) public returns(bool) {}

rule TransferFromChecksAndEffects() {
    address $from;
    address $to;
    uint256 $value;
    __assume__(balanceOf[$from] >= $value);
    __assume__(allowance[$from][msg.sender] >= $value);

    uint256 balanceFromBefore = balanceOf[$from];
    uint256 balanceToBefore = balanceOf[$to];
    uint256 allowanceBefore = allowance[$from][msg.sender];

    transferFrom($from, $to, $value);

    assert(balanceOf[$from] == balanceFromBefore - $value);
    assert(balanceOf[$to] == balanceToBefore + $value);
    assert(allowance[$from][msg.sender] == allowanceBefore - $value);
}}