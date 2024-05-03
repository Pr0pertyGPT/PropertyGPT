// SPDX-License-Identifier: agpl-3.0
pragma solidity 0.8.17;
//pragma solidity 0.8.15;
import {IERC20} from '../../src/interfaces/IERC20.sol';

contract DummyERC20Impl is IERC20 {
  address internal _owner;

  constructor(address owner_) {
    _owner = owner_;
  }

  modifier onlyOwner() {
    require(msg.sender == _owner, 'only owner can access');
    _;
  }

  function owner() public view returns (address) {
    return _owner;
  }

  uint256 t;
  mapping(address => uint256) b;
  mapping(address => mapping(address => uint256)) a;

  string public name;
  string public symbol;
  uint256 public decimals;

  function myAddress() public returns (address) {
    return address(this);
  }

  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    require(c >= a);
    return c;
  }

  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    require(a >= b);
    return a - b;
  }

  function totalSupply() public view override returns (uint256) {
    return t;
  }

  function balanceOf(address account) public view override returns (uint256) {
    return b[account];
  }

  function transfer(address recipient, uint256 amount)
    external
    override
    returns (bool)
  {
    b[msg.sender] = sub(b[msg.sender], amount);
    b[recipient] = add(b[recipient], amount);
    return true;
  }

  function allowance(address owner, address spender)
    external
    view
    override
    returns (uint256)
  {
    return a[owner][spender];
  }

  function approve(address spender, uint256 amount)
    external
    override
    returns (bool)
  {
    a[msg.sender][spender] = amount;
    return true;
  }

  function transferFrom(
    address sender,
    address recipient,
    uint256 amount
  ) external override returns (bool) {
    b[sender] = sub(b[sender], amount);
    b[recipient] = add(b[recipient], amount);
    a[sender][msg.sender] = sub(a[sender][msg.sender], amount);
    return true;
  }
}
