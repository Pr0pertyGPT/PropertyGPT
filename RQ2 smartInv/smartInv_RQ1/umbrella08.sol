// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

contract VulnerableStaking {
    mapping(address => uint256) public balances;
    uint256 public totalSupply;

    event Withdrawn(address indexed user, uint256 amount);

    constructor() {
        totalSupply = 1000; // 初始总供应量
    }

    // 模拟存款，简单地增加用户余额和总供应量
    function deposit(uint256 amount) public {
        balances[msg.sender] += amount;
        totalSupply += amount;
    }

    // 存在漏洞的提款函数
    function withdraw(uint256 amount) public {
        require(amount != 0, "Cannot withdraw 0");
        require(balances[msg.sender] >= amount, "Insufficient balance"); // 正常情况下应该有的检查

        unchecked {
            // 使用 unchecked 来绕过 Solidity 0.8.0 的溢出/下溢检查
            balances[msg.sender] -= amount;
            totalSupply -= amount;
        }

        emit Withdrawn(msg.sender, amount);
    }

    // 查看账户余额
    function balanceOf(address account) public view returns (uint256) {
        return balances[account];
    }

    // 查看总供应量
    function totalSupplyOf() public view returns (uint256) {
        return totalSupply;
    }
}
