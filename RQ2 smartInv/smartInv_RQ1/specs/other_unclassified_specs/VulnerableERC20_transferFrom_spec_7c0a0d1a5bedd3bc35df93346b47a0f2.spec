pragma solidity 0.8.0;

contract VulnerableERC20 {mapping(address => uint256) private _balances;
mapping(address => mapping(address => uint256)) private _allowances;
uint256 private _totalSupply;
string private _name;
string private _symbol;
uint8 private _decimals;

function allowance(address,address) public returns(uint256) {}
function transferFrom(address,address,uint256) public returns(bool) {}

rule ValidateTransferFromDecrementAllowance() {
    address $sender;
    address $recipient;
    uint256 $amount;
    uint256 allowanceBefore = allowance($sender, $recipient);
    
    __assume__(msg.sender == $sender);
    transferFrom($sender, $recipient, $amount);

    assert(allowance($sender, $recipient) == (allowanceBefore - $amount));
}}