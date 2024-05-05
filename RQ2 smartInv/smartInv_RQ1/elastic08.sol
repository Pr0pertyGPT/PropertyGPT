// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.0;

/**
 * @title ElasticTokenSwap
 * @dev Demonstration of a rebase logic flaw in liquidity pools with elastic supply tokens
 */
contract ElasticTokenSwap {
    uint256 public baseTokenReserve;
    uint256 public quoteTokenReserve;
    uint256 public totalLiquidity;
    uint256 public baseTokenTotalSupply;

    mapping(address => uint256) public liquidityBalance;

    event LiquidityAdded(address indexed provider, uint256 baseAmount, uint256 quoteAmount);
    event LiquidityRemoved(address indexed provider, uint256 baseAmount, uint256 quoteAmount);

    constructor() {
        baseTokenReserve = 1000;
        quoteTokenReserve = 500;
        baseTokenTotalSupply = 1000;  // Initial supply
    }

    // Function to simulate the rebase of token supply
    function rebase(uint256 newSupply) public {
        baseTokenTotalSupply = newSupply;
    }

    // Add liquidity to the pool
    function addLiquidity(uint256 baseAmount, uint256 quoteAmount) public {
        require(baseAmount > 0 && quoteAmount > 0, "Amounts must be greater than zero");

        uint256 liquidityIssued = (baseAmount + quoteAmount) * totalLiquidity / (baseTokenReserve + quoteTokenReserve);
        if (totalLiquidity == 0) {
            liquidityIssued = baseAmount + quoteAmount;  // Initial liquidity provision
        }

        baseTokenReserve += baseAmount;
        quoteTokenReserve += quoteAmount;

        totalLiquidity += liquidityIssued;
        liquidityBalance[msg.sender] += liquidityIssued;

        emit LiquidityAdded(msg.sender, baseAmount, quoteAmount);
    }

    // Remove liquidity from the pool
    function removeLiquidity(uint256 liquidity) public {
        require(liquidity > 0 && liquidity <= liquidityBalance[msg.sender], "Invalid liquidity amount");
        require(totalLiquidity > 0, "No liquidity available");

        uint256 baseAmount = (liquidity * baseTokenReserve) / totalLiquidity;
        uint256 quoteAmount = (liquidity * quoteTokenReserve) / totalLiquidity;

        baseTokenReserve -= baseAmount;
        quoteTokenReserve -= quoteAmount;

        totalLiquidity -= liquidity;
        liquidityBalance[msg.sender] -= liquidity;

        emit LiquidityRemoved(msg.sender, baseAmount, quoteAmount);
    }
}
