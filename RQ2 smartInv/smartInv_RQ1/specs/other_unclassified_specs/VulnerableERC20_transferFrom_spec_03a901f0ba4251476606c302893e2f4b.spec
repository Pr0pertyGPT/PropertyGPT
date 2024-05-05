pragma solidity 0.8.0;

contract VulnerableERC20 {mapping(address => uint256) private _balances;
mapping(address => mapping(address => uint256)) private _allowances;
uint256 private _totalSupply;
string private _name;
string private _symbol;
uint8 private _decimals;

function allowance(address,address) public returns(uint256) {}
function transferFrom(address,address,uint256) public returns(bool) {}

rule TransferFromReducesAllowance() {
    address $sender;
    address $recipient;
    uint256 $amount;

    __assume__(msg.sender != $sender);
    __assume__(msg.sender != $recipient);

    uint256 allowanceBefore = allowance($sender, msg.sender);
    transferFrom($sender, $recipient, $amount);
    uint256 allowanceAfter = allowance($sender, msg.sender);

    assert(allowanceBefore - $amount == allowanceAfter);
}}