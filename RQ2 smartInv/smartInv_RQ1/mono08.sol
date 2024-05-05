// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimplifiedLiquidityPool {
    address public owner;
    mapping(address => mapping(address => uint256)) public liquidityBalance;

    event LiquidityRemoved(address indexed token, address indexed to, uint256 amount);

    function addLiquidity(address token, uint256 amount) external {
        liquidityBalance[token][msg.sender] += amount;
    }

    function removeLiquidity(address token, address to, uint256 amount) external {
        require(liquidityBalance[token][to] >= amount, "Insufficient liquidity");

        liquidityBalance[token][to] -= amount;

        emit LiquidityRemoved(token, to, amount);
    }
}
