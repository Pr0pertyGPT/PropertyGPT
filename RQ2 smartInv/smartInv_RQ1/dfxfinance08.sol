// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

contract SimpleCurve {
    mapping(address => uint256) public balances;
    mapping(address => bool) public isBorrowed;
    uint256 public totalLiquidity;

    event FlashLoan(address borrower, uint256 amount, bool isPaidBack);
    event Deposit(address depositor, uint256 amount);
    event Withdrawal(address withdrawer, uint256 amount);

    constructor() {
        totalLiquidity = 0;
    }

    function flashLoan(uint256 amount) public {
        require(balances[address(this)] >= amount, "Not enough liquidity");
        
        balances[msg.sender] += amount;
        balances[address(this)] -= amount;

        isBorrowed[msg.sender] = true;


        require(balances[address(this)] >= amount, "Loan not repaid");
        
        isBorrowed[msg.sender] = false;

        emit FlashLoan(msg.sender, amount, true);
    }

    function deposit(uint256 amount) public {
        balances[msg.sender] += amount;
        balances[address(this)] += amount;
        totalLiquidity += amount;
        
        emit Deposit(msg.sender, amount);
    }

    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        require(totalLiquidity >= amount, "Insufficient liquidity");

        balances[msg.sender] -= amount;
        balances[address(this)] -= amount;
        totalLiquidity -= amount;

        emit Withdrawal(msg.sender, amount);
    }

    function balanceOf(address account) public view returns (uint256) {
        return balances[account];
    }

    function getLiquidity() public view returns (uint256) {
        return totalLiquidity;
    }
}
