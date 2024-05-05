pragma solidity 0.8.0;

contract VulnerableERC20 {mapping(address => uint256) private _balances;
mapping(address => mapping(address => uint256)) private _allowances;
uint256 private _totalSupply;
string private _name;
string private _symbol;
uint8 private _decimals;

function allowance(address,address) public returns(uint256) {}
function approve(address,uint256) public returns(bool) {}
function transferFrom(address,address,uint256) public returns(bool) {}
function _approve(address,address,uint256) public  {}

rule TransferFromCorrectlyUpdatesAllowance() {
    address $sender;
    address $recipient;
    uint256 $amount;
    uint256 $init_allowance;
    
    __assume__(msg.sender == 0x0000000000000000000000000000000000000001);
    _approve($sender, $recipient, $init_allowance);

    transferFrom($sender, $recipient, $amount);

    if ($sender != msg.sender) {
        assert(allowance($sender, $recipient) == ($init_allowance - $amount));
    } else {
        assert(allowance($sender, $recipient) == $init_allowance);
    }
}}