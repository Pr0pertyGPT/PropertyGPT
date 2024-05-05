pragma solidity 0.8.0;

contract VulnerableERC20 {mapping(address => uint256) private _balances;
mapping(address => mapping(address => uint256)) private _allowances;
uint256 private _totalSupply;
string private _name;
string private _symbol;
uint8 private _decimals;

function balanceOf(address) public returns(uint256) {}
function transferFrom(address,address,uint256) public returns(bool) {}

rule TransferFromDoesNotAlterTotalBalance() {
    address $sender;
    address $recipient;
    uint256 $amount;
    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);

    uint256 balanceSenderBefore = balanceOf($sender);
    uint256 balanceRecipientBefore = balanceOf($recipient);
    transferFrom($sender, $recipient, $amount);
    uint256 balanceSenderAfter = balanceOf($sender);
    uint256 balanceRecipientAfter = balanceOf($recipient);
    
    // The sum of sender's and recipient's balances before and after should remain same, indicating no loss/gain in total supply
    assert(balanceSenderBefore + balanceRecipientBefore == balanceSenderAfter + balanceRecipientAfter);
}}