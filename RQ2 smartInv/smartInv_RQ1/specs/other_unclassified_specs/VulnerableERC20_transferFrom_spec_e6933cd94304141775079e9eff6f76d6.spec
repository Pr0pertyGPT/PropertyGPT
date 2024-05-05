pragma solidity 0.8.0;

contract VulnerableERC20 {mapping(address => uint256) private _balances;
mapping(address => mapping(address => uint256)) private _allowances;
uint256 private _totalSupply;
string private _name;
string private _symbol;
uint8 private _decimals;

function balanceOf(address) public returns(uint256) {}
function allowance(address,address) public returns(uint256) {}
function transferFrom(address,address,uint256) public returns(bool) {}

rule TransferFromBalanceConsistency() {
    address $sender;
    address $recipient;
    uint256 $amount;

    // Preconditions
    __assume__($sender != $recipient);
    __assume__($amount > 0);

    uint256 balanceSenderBefore = balanceOf($sender);
    uint256 balanceRecipientBefore = balanceOf($recipient);
    uint256 allowanceBefore = allowance($sender, $recipient);

    // Execute function
    transferFrom($sender, $recipient, $amount);

    // Postconditions
    assert(balanceOf($sender) == balanceSenderBefore - $amount);
    assert(balanceOf($recipient) == balanceRecipientBefore + $amount);
    assert(allowance($sender, $recipient) == allowanceBefore - $amount);
}}