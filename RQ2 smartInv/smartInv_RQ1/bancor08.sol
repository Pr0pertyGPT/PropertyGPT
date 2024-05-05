// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableBancor {
    mapping(address => mapping(address => uint256)) public allowance;
    mapping(address => uint256) public balanceOf;

    constructor() {
        // 给部署合约的地址一些初始代币供测试
        balanceOf[msg.sender] = 10000;
    }

    // 模拟 ERC-20 的 approve 函数
    function approve(address spender, uint256 amount) public returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    // 模拟 ERC-20 的 transferFrom 函数
    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(balanceOf[from] >= value, "Insufficient balance");
        require(allowance[from][msg.sender] >= value, "Insufficient allowance");

        balanceOf[from] -= value;
        balanceOf[to] += value;
        allowance[from][msg.sender] -= value;
        return true;
    }

    // 漏洞函数：任何人可以调用，没有适当的权限检查
    function safeTransferFrom(address _token, address _from, address _to, uint256 _value) public {
        // 这里调用 transferFrom，但在现实应用中应该有更多的安全检查
        transferFrom(_from, _to, _value);
    }
}
