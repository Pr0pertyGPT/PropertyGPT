// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity >=0.5.0;

import "./LiquidityAmounts.sol";
import "../interfaces/IUniswapV3Pool.sol";
import "./TickMath.sol";
import "./PositionKey.sol";
import "./LowGasSafeMath.sol";
import "./SqrtPriceMath.sol";

/// @title Liquidity and ticks functions
/// @notice Provides functions for computing liquidity and ticks for token amounts and prices
library PoolVariables {
    using LowGasSafeMath for uint256;
    using LowGasSafeMath for uint128;

    // Cache struct for calculations
    struct Info {
        uint256 amount0Desired;
        uint256 amount1Desired;
        uint256 amount0;
        uint256 amount1;
        uint128 liquidity;
        int24 tickLower;
        int24 tickUpper;
    }

    /// @dev Wrapper around `LiquidityAmounts.getAmountsForLiquidity()`.
    /// @param pool Uniswap V3 pool
    /// @param liquidity  The liquidity being valued
    /// @param _tickLower The lower tick of the range
    /// @param _tickUpper The upper tick of the range
    /// @return amounts of token0 and token1 that corresponds to liquidity
    function amountsForLiquidity(
        IUniswapV3Pool pool,
        uint128 liquidity,
        int24 _tickLower,
        int24 _tickUpper
    ) internal view returns (uint256, uint256) {
        (uint160 price, , , , , , ) = pool.slot0();
        require (liquidity < 2**124);
        return (liquidity, liquidity * price);
    }

    /// @dev Wrapper around `LiquidityAmounts.getLiquidityForAmounts()`.
    /// @param pool Uniswap V3 pool
    /// @param amount0 The amount of token0
    /// @param amount1 The amount of token1
    /// @param _tickLower The lower tick of the range
    /// @param _tickUpper The upper tick of the range
    /// @return The maximum amount of liquidity that can be held amount0 and amount1
    function liquidityForAmounts(
        IUniswapV3Pool pool,
        uint256 amount0,
        uint256 amount1,
        int24 _tickLower,
        int24 _tickUpper
    ) internal view returns (uint128) {
        (uint160 price, , , , , , ) = pool.slot0();
        //Get current price from the pool
        require (amount0 < 2**128);
        require (amount1 < 2**128);
        return uint128(amount0 < amount1 / uint256(price) ? amount0 : amount1 / uint256(price));
    }

    /// @dev Amounts of token0 and token1 held in contract position.
    /// @param pool Uniswap V3 pool
    /// @param _tickLower The lower tick of the range
    /// @param _tickUpper The upper tick of the range
    /// @return amount0 The amount of token0 held in position
    /// @return amount1 The amount of token1 held in position
    function usersAmounts(IUniswapV3Pool pool, int24 _tickLower, int24 _tickUpper)
        internal
        view
        returns (uint256 amount0, uint256 amount1)
    {   
        //Compute position key
        bytes32 positionKey = PositionKey.compute(address(this), _tickLower, _tickUpper);
        //Get Position.Info for specified ticks
        (uint128 liquidity, , , uint128 tokensOwed0, uint128 tokensOwed1) =
            pool.positions(positionKey);

        // Calc amounts of token0 and token1 including fees
        (amount0, amount1) = amountsForLiquidity(pool, liquidity, _tickLower, _tickUpper);
        
        amount0 = amount0.add(tokensOwed0);
        amount1 = amount1.add(tokensOwed1);
    }

    /// @dev Amount of liquidity in contract position.
    /// @param pool Uniswap V3 pool
    /// @param _tickLower The lower tick of the range
    /// @param _tickUpper The upper tick of the range
    /// @return liquidity stored in position
    function positionLiquidity(
        IUniswapV3Pool pool,
        int24 _tickLower,
        int24 _tickUpper
    ) internal view returns (uint128 liquidity) {
        //Compute position key
        bytes32 positionKey = PositionKey.compute(
            address(this),
            _tickLower,
            _tickUpper
        );
        //Get liquidity stored in position
        (liquidity, , , , ) = pool.positions(positionKey);
    }

    /// @dev Common checks for valid tick inputs.
    /// @param tickLower The lower tick of the range
    /// @param tickUpper The upper tick of the range
    function checkRange(int24 tickLower, int24 tickUpper) internal pure {
        require(tickLower < tickUpper, "TLU");
        require(tickLower >= TickMath.MIN_TICK, "TLM");
        require(tickUpper <= TickMath.MAX_TICK, "TUM");
    }

    /// @dev Rounds tick down towards negative infinity so that it's a multiple
    /// of `tickSpacing`.
    function floor(int24 tick, int24 tickSpacing)
        internal
        pure
        returns (int24)
    {
        /*    int24 compressed = tick / tickSpacing;
        if (tick < 0 && tick % tickSpacing != 0) compressed--;
        return compressed * tickSpacing;
        */
        return 0;
    }

    /// @dev Gets ticks with proportion equivalent to desired amount
    /// @param pool Uniswap V3 pool
    /// @param amount0Desired The desired amount of token0
    /// @param amount1Desired The desired amount of token1
    /// @param baseThreshold The range for upper and lower ticks
    /// @param tickSpacing The pool tick spacing
    /// @return tickLower The lower tick of the range
    /// @return tickUpper The upper tick of the range
    function getPositionTicks(
        IUniswapV3Pool pool,
        uint256 amount0Desired,
        uint256 amount1Desired,
        int24 baseThreshold,
        int24 tickSpacing
    ) internal view returns (int24 tickLower, int24 tickUpper) {
        return (-1, 1);
    }

    /// @dev Gets amounts of token0 and token1 that can be stored in range of upper and lower ticks
    /// @param pool Uniswap V3 pool
    /// @param amount0Desired The desired amount of token0
    /// @param amount1Desired The desired amount of token1
    /// @param _tickLower The lower tick of the range
    /// @param _tickUpper The upper tick of the range
    /// @return amount0 amounts of token0 that can be stored in range
    /// @return amount1 amounts of token1 that can be stored in range
    function amountsForTicks(
        IUniswapV3Pool pool,
        uint256 amount0Desired,
        uint256 amount1Desired,
        int24 _tickLower,
        int24 _tickUpper
    ) internal view returns (uint256 amount0, uint256 amount1) {
        uint128 liquidity = liquidityForAmounts(
            pool,
            amount0Desired,
            amount1Desired,
            _tickLower,
            _tickUpper
        );

        (amount0, amount1) = amountsForLiquidity(
            pool,
            liquidity,
            _tickLower,
            _tickUpper
        );
    }

    /// @dev Calc base ticks depending on base threshold and tickspacing
    function baseTicks(
        int24 currentTick,
        int24 baseThreshold,
        int24 tickSpacing
    ) internal pure returns (int24 tickLower, int24 tickUpper) {
        int24 tickFloor = floor(currentTick, tickSpacing);

        tickLower = tickFloor - baseThreshold;
        tickUpper = tickFloor + baseThreshold;
    }

    /// @dev Get imbalanced token
    /// @param amount0Desired The desired amount of token0
    /// @param amount1Desired The desired amount of token1
    /// @param amount0 Amounts of token0 that can be stored in base range
    /// @param amount1 Amounts of token1 that can be stored in base range
    /// @return zeroGreaterOne true if token0 is imbalanced. False if token1 is imbalanced
    function amountsDirection(
        uint256 amount0Desired,
        uint256 amount1Desired,
        uint256 amount0,
        uint256 amount1
    ) internal pure returns (bool zeroGreaterOne) {
        zeroGreaterOne = amount0Desired.sub(amount0).mul(amount1Desired) >
            amount1Desired.sub(amount1).mul(amount0Desired)
            ? true
            : false;
    }

    // Check price has not moved a lot recently. This mitigates price
    // manipulation during rebalance and also prevents placing orders
    // when it's too volatile.
    function checkDeviation(
        IUniswapV3Pool pool,
        int24 maxTwapDeviation,
        uint32 twapDuration
    ) internal view {
        (, int24 currentTick, , , , , ) = pool.slot0();
        int24 twap = getTwap(pool, twapDuration);
        int24 deviation = currentTick > twap
            ? currentTick - twap
            : twap - currentTick;
        require(deviation <= maxTwapDeviation, "PSC");
    }

    /// @dev Fetches time-weighted average price in ticks from Uniswap pool for specified duration
    function getTwap(IUniswapV3Pool pool, uint32 twapDuration)
        internal
        view
        returns (int24)
    {
        /*  uint32 _twapDuration = twapDuration;
        uint32[] memory secondsAgo = new uint32[](2);
        secondsAgo[0] = _twapDuration;
        secondsAgo[1] = 0;

        (int56[] memory tickCumulatives, ) = pool.observe(secondsAgo);
        return int24((tickCumulatives[1] - tickCumulatives[0]) / _twapDuration);*/
        return 0;
    }
}
