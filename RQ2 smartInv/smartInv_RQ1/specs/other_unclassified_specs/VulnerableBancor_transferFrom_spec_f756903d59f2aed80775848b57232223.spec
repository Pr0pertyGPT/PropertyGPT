pragma solidity 0.8.0;

contract VulnerableBancor {mapping(address => mapping(address => uint256)) public allowance;
mapping(address => uint256) public balanceOf;

function transferFrom(address,address,uint256) public returns(bool) {}

rule VerifyCorrectnessOfTransferFromFunction() {
    address $from;
    address $to;
    uint256 $value;
    uint256 $allowanceBefore = allowance[$from][msg.sender];
    uint256 $balanceOfFromBefore = balanceOf[$from];
    uint256 $balanceOfToBefore = balanceOf[$to];

    // Set up assumptions necessary for transferFrom to succeed
    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);
    __assume__(allowance[$from][msg.sender] >= $value);
    __assume__(balanceOf[$from] >= $value);

    // Execute the transferFrom function
    transferFrom($from, $to, $value);

    // Verify the post-conditions after transferFrom execution
    assert(balanceOf[$from] == $balanceOfFromBefore - $value);
    assert(balanceOf[$to] == $balanceOfToBefore + $value);
    assert(allowance[$from][msg.sender] == $allowanceBefore - $value);
}}