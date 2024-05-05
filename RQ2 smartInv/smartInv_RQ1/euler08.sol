// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableReserve {
    mapping(address => uint256) public balances;
    mapping(address => uint256) public debts;
    uint256 public totalReserve;

    event Donate(address indexed user, uint256 amount);
    event DebtNotReduced(address indexed user, uint256 debtAmount);

    function donateToReserves(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");

        balances[msg.sender] -= amount; 
        totalReserve += amount;         

        emit Donate(msg.sender, amount);

    }

    function deposit(uint256 amount) public {
        balances[msg.sender] += amount;
    }

    function borrow(uint256 amount) public {
        balances[msg.sender] += amount;  
        debts[msg.sender] += amount;    
    }

    function repay(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        require(debts[msg.sender] >= amount, "Debt is less than amount");

        balances[msg.sender] -= amount;
        debts[msg.sender] -= amount;
    }

    function getBalance(address user) public view returns (uint256) {
        return balances[user];
    }

    function getDebt(address user) public view returns (uint256) {
        return debts[user];
    }

    function getReserve() public view returns (uint256) {
        return totalReserve;
    }
}
