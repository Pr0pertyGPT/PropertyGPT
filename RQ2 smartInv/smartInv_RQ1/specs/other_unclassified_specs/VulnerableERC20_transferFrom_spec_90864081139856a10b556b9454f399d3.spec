pragma solidity 0.8.0;

contract VulnerableERC20 {mapping(address => uint256) private _balances;
mapping(address => mapping(address => uint256)) private _allowances;
uint256 private _totalSupply;
string private _name;
string private _symbol;
uint8 private _decimals;

function transferFrom(address,address,uint256) public returns(bool) {}

rule TransferFromBalanceConsistency() {
    address $sender;
    address $recipient;
    uint256 $amount;
    uint256 $senderInitialBalance;
    uint256 $recipientInitialBalance;
    uint256 $senderAllowance;

    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);

    _balances[$sender] = $senderInitialBalance;
    _balances[$recipient] = $recipientInitialBalance;
    _allowances[$sender][msg.sender] = $senderAllowance;

    uint256 senderBalanceBefore = _balances[$sender];
    uint256 recipientBalanceBefore = _balances[$recipient];
    uint256 senderAllowanceBefore = _allowances[$sender][msg.sender];

    transferFrom($sender, $recipient, $amount);

    assert(_balances[$sender] == senderBalanceBefore - $amount);
    assert(_balances[$recipient] == recipientBalanceBefore + $amount);
    assert(_allowances[$sender][msg.sender] == senderAllowanceBefore - $amount);
}}