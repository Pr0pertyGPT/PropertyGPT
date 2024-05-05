pragma solidity 0.8.0;

contract VulnerableERC20 {mapping(address => uint256) private _balances;
mapping(address => mapping(address => uint256)) private _allowances;
uint256 private _totalSupply;
string private _name;
string private _symbol;
uint8 private _decimals;

function allowance(address,address) public returns(uint256) {}
function transferFrom(address,address,uint256) public returns(bool) {}

rule ValidateTransferFromEnsuresAllowanceConsistency(){
    address $sender;
    address $recipient;
    uint256 $amount;
    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);
    uint256 allowanceBefore = allowance($sender, $recipient);
    transferFrom($sender, $recipient, $amount);
    uint256 allowanceAfter = allowance($sender, $recipient);
    assert(allowanceBefore - $amount == allowanceAfter);
}}