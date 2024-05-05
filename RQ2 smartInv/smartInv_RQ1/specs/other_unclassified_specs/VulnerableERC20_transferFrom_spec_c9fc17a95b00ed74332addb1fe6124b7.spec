pragma solidity 0.8.0;

contract VulnerableERC20{mapping(address => uint256) private _balances;
mapping(address => mapping(address => uint256)) private _allowances;
uint256 private _totalSupply;
string private _name;
string private _symbol;
uint8 private _decimals;
function transferFrom(address,address,uint256) public returns(bool) 
precondition{
    _balances[sender] >= amount ? true : false;
    _allowances[sender][msg.sender] >= amount ? true : false;
}

postcondition{
    __old__(_balances[sender]) - amount == _balances[sender] ? true : false;
    __old__(_balances[recipient]) + amount == _balances[recipient] ? true : false;
    __old__(_allowances[sender][msg.sender]) - amount == _allowances[sender][msg.sender] ? true : false;
}
}