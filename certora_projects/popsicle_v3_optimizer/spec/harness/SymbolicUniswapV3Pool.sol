import "../../contracts/popsicle-v3-optimizer/interfaces/IUniswapV3Pool.sol";
import "../../contracts/popsicle-v3-optimizer/token/IERC20.sol";
import "../../contracts/popsicle-v3-optimizer/libraries/LowGasSafeMath.sol";
import "../../contracts/popsicle-v3-optimizer/libraries/PoolActions.sol";

/// @title Callback for IUniswapV3PoolActions#mint
/// @notice Any contract that calls IUniswapV3PoolActions#mint must implement this interface
interface IUniswapV3MintCallback {
    /// @notice Called to `msg.sender` after minting liquidity to a position from IUniswapV3Pool#mint.
    /// @dev In the implementation you must pay the pool tokens owed for the minted liquidity.
    /// The caller of this method must be checked to be a UniswapV3Pool deployed by the canonical UniswapV3Factory.
    /// @param amount0Owed The amount of token0 due to the pool for the minted liquidity
    /// @param amount1Owed The amount of token1 due to the pool for the minted liquidity
    /// @param data Any data passed through by the caller via the IUniswapV3PoolActions#mint call
    function uniswapV3MintCallback(
        uint256 amount0Owed,
        uint256 amount1Owed,
        bytes calldata data
    ) external;
}

/// @title Callback for IUniswapV3PoolActions#swap
/// @notice Any contract that calls IUniswapV3PoolActions#swap must implement this interface
interface IUniswapV3SwapCallback {
    /// @notice Called to `msg.sender` after executing a swap via IUniswapV3Pool#swap.
    /// @dev In the implementation you must pay the pool tokens owed for the swap.
    /// The caller of this method must be checked to be a UniswapV3Pool deployed by the canonical UniswapV3Factory.
    /// amount0Delta and amount1Delta can both be 0 if no tokens were swapped.
    /// @param amount0Delta The amount of token0 that was sent (negative) or must be received (positive) by the pool by
    /// the end of the swap. If positive, the callback must send that amount of token0 to the pool.
    /// @param amount1Delta The amount of token1 that was sent (negative) or must be received (positive) by the pool by
    /// the end of the swap. If positive, the callback must send that amount of token1 to the pool.
    /// @param data Any data passed through by the caller via the IUniswapV3PoolActions#swap call
    function uniswapV3SwapCallback(
        int256 amount0Delta,
        int256 amount1Delta,
        bytes calldata data
    ) external;
}

contract SymbolicUniswapV3Pool is IUniswapV3Pool {
    uint256 public liquidity;
    uint256 public ratio;
    address public immutable override token0;
    address public immutable override token1;
    uint128 public owed0;
    uint128 public owed1;
    using LowGasSafeMath for uint256;
    using LowGasSafeMath for uint128;
    using LowGasSafeMath for int256;
    using PoolVariables for IUniswapV3Pool;

    constructor(address _token0, address _token1) {
        token0 = _token0;
        token1 = _token1;
        ratio = 4;
    }

    function balance0() public view returns (uint256) {
        return IERC20(token0).balanceOf(address(this));
    }

    /// @dev Get the pool's balance of token1
    /// @dev This function is gas optimized to avoid a redundant extcodesize check in addition to the returndatasize
    /// check
    function balance1() public view returns (uint256) {
        return IERC20(token1).balanceOf(address(this));
    }


     function liquidityForAmounts(
        IUniswapV3Pool pool,
        uint256 amount0,
        uint256 amount1,
        int24 _tickLower,
        int24 _tickUpper
    ) public view returns (uint128) {
        return pool.liquidityForAmounts(amount0, amount1, _tickLower, _tickUpper);
    }

    /// @notice Adds liquidity for the given recipient/tickLower/tickUpper position
    /// @dev The caller of this method receives a callback in the form of IUniswapV3MintCallback#uniswapV3MintCallback
    /// in which they must pay any token0 or token1 owed for the liquidity. The amount of token0/token1 due depends
    /// on tickLower, tickUpper, the amount of liquidity, and the current price.
    /// @param recipient The address for which the liquidity will be created
    /// @param tickLower The lower tick of the position in which to add liquidity
    /// @param tickUpper The upper tick of the position in which to add liquidity
    /// @param amount The amount of liquidity to mint
    /// @param data Any data that should be passed through to the callback
    /// @return amount0 The amount of token0 that was paid to mint the given amount of liquidity. Matches the value in the callback
    /// @return amount1 The amount of token1 that was paid to mint the given amount of liquidity. Matches the value in the callback
    function mint(
        address recipient,
        int24 tickLower,
        int24 tickUpper,
        uint128 amount,
        bytes calldata data
    ) external override returns (uint256 amount0, uint256 amount1) {
        require(ratio == 1 || ratio == 2 || ratio == 4);
        liquidity = liquidity.add(amount);
        amount0 = amount;
        amount1 = uint256(amount).mul(ratio);
        uint256 token0Balance = balance0();
        uint256 token1Balance = balance1();
        IUniswapV3MintCallback(msg.sender).uniswapV3MintCallback(
            amount0,
            amount1,
            data
        );
        //maybe add require that now the balance increased as expected
        require(balance0() >= token0Balance.add(amount0));
        require(balance1() >= token1Balance.add(amount1));
    }

    /// @notice Collects tokens owed to a position
    /// @dev Does not recompute fees earned, which must be done either via mint or burn of any amount of liquidity.
    /// Collect must be called by the position owner. To withdraw only token0 or only token1, amount0Requested or
    /// amount1Requested may be set to zero. To withdraw all tokens owed, caller may pass any value greater than the
    /// actual tokens owed, e.g. type(uint128).max. Tokens owed may be from accumulated swap fees or burned liquidity.
    /// @param recipient The address which should receive the fees collected
    /// @param tickLower The lower tick of the position for which to collect fees
    /// @param tickUpper The upper tick of the position for which to collect fees
    /// @param amount0Requested How much token0 should be withdrawn from the fees owed
    /// @param amount1Requested How much token1 should be withdrawn from the fees owed
    /// @return amount0 The amount of fees collected in token0
    /// @return amount1 The amount of fees collected in token1
    function collect(
        address recipient,
        int24 tickLower,
        int24 tickUpper,
        uint128 amount0Requested,
        uint128 amount1Requested
    ) external override returns (uint128 amount0, uint128 amount1) {
        if (amount0Requested >= owed0) {
            amount0 = owed0;
            owed0 = 0;
        } else {
            owed0 = owed0.sub128(amount0Requested);
            amount0 = amount0Requested;
        }
        IERC20(token0).transfer(recipient, amount0);
        if (amount1Requested >= owed1) {
            amount1 = owed1;
            owed1 = 0;
        } else {
            owed1 = owed1.sub128(amount1Requested);
            amount1 = amount1Requested;
        }
        IERC20(token1).transfer(recipient, amount1);
    }

    /// @notice Burn liquidity from the sender and account tokens owed for the liquidity to the position
    /// @dev Can be used to trigger a recalculation of fees owed to a position by calling with an amount of 0
    /// @dev Fees must be collected separately via a call to #collect
    /// @param tickLower The lower tick of the position for which to burn liquidity
    /// @param tickUpper The upper tick of the position for which to burn liquidity
    /// @param amount How much liquidity to burn
    /// @return amount0 The amount of token0 sent to the recipient
    /// @return amount1 The amount of token1 sent to the recipient
    function burn(
        int24 tickLower,
        int24 tickUpper,
        uint128 amount
    ) external override returns (uint256 amount0, uint256 amount1) {
        require(ratio == 1 || ratio == 2 || ratio == 4);
        require(liquidity >= amount);
        amount0 = amount;
        amount1 = amount.mul(ratio);
        liquidity = liquidity.sub(amount);

        require(amount0 < 2**128);
        require(amount1 < 2**128);

        owed0 = owed0.add128(uint128(amount0));
        owed1 = owed1.add128(uint128(amount1));
    }

    /// @notice Swap token0 for token1, or token1 for token0, rate does not change so limit amout to 100, and pool creator must tarnsfer to it huge amount of token0 and token1
    /// @dev The caller of this method receives a callback in the form of IUniswapV3SwapCallback#uniswapV3SwapCallback
    /// @param recipient The address to receive the output of the swap
    /// @param zeroForOne The direction of the swap, true for token0 to token1, false for token1 to token0
    /// @param amountSpecified The amount of the swap, which implicitly configures the swap as exact input (positive), or exact output (negative)
    /// @param sqrtPriceLimitX96 The Q64.96 sqrt price limit. If zero for one, the price cannot be less than this
    /// value after the swap. If one for zero, the price cannot be greater than this value after the swap
    /// @param data Any data to be passed through to the callback
    /// @return amount0 The delta of the balance of token0 of the pool, exact when negative, minimum when positive
    /// @return amount1 The delta of the balance of token1 of the pool, exact when negative, minimum when positive
    function swap(
        address recipient,
        bool zeroForOne,
        int256 amountSpecified,
        uint160 sqrtPriceLimitX96,
        bytes calldata data
    ) external override returns (int256 amount0, int256 amount1) {
        bool exactInput = amountSpecified > 0;
        if (!exactInput) amountSpecified = -amountSpecified;
        int256 amountToPay = exactInput
            ? amountSpecified
            : (
                zeroForOne
                    ? amountSpecified / int256(ratio)
                    : amountSpecified.mul(int256(ratio))
            );
        int256 amountToGet = exactInput
            ? (
                zeroForOne
                    ? amountSpecified.mul(int256(ratio))
                    : amountSpecified / int256(ratio)
            )
            : amountSpecified;
        // do the transfers and collect payment
        // amountToGet = amountToGet.mul(99) / 100;
        if (zeroForOne) {
            require(amountToGet >= 0);
            uint256 temp = uint256(amountToGet);
            require(temp < 2**128);
            // owed1 = owed1.add128(uint128(uint256(amountToGet) / 100));
            IERC20(token1).transfer(recipient, uint256(amountToGet));
            uint256 balance0Before = balance0();
            IUniswapV3SwapCallback(msg.sender).uniswapV3SwapCallback(
                amountToPay,
                -amountToGet,
                data
            );
            require(
                balance0Before.add(uint256(amountToPay)) <= balance0(),
                "IIA"
            );
        } else {
            require(amountToGet >= 0);
            uint256 temp = uint256(amountToGet);
            require(temp < 2**128);
            // owed0 = owed0.add128(uint128(uint256(amountToGet) / 100));
            IERC20(token0).transfer(recipient, uint256(amountToGet));
            uint256 balance1Before = balance1();
            IUniswapV3SwapCallback(msg.sender).uniswapV3SwapCallback(
                -amountToGet,
                amountToPay,
                data
            );
            require(
                balance1Before.add(uint256(amountToPay)) <= balance1(),
                "IIA"
            );
        }
        if (ratio == 4) {
            ratio = 2;
        } else if (ratio == 2) {
            ratio = 1;
        } else {
            ratio = 4;
        }
    }

    /// @notice Returns the cumulative tick and liquidity as of each timestamp `secondsAgo` from the current block timestamp
    /// @dev To get a time weighted average tick or liquidity-in-range, you must call this with two values, one representing
    /// the beginning of the period and another for the end of the period. E.g., to get the last hour time-weighted average tick,
    /// you must call it with secondsAgo = [3600, 0].
    /// @dev The time weighted average tick represents the geometric time weighted average price of the pool, in
    /// log base sqrt(1.0001) of token1 / token0. The TickMath library can be used to go from a tick value to a ratio.
    /// @param secondsAgo From how long ago each cumulative tick and liquidity value should be returned
    /// @return tickCumulatives Cumulative tick values as of each `secondsAgo` from the current block timestamp
    /// @return secondsPerLiquidityCumulativeX128s Cumulative seconds per liquidity-in-range value as of each `secondsAgo` from the current block
    /// timestamp
    function observe(uint32[] calldata secondsAgo)
        external
        view
        override
        returns (
            int56[] memory tickCumulatives,
            uint160[] memory secondsPerLiquidityCumulativeX128s
        )
    {
        tickCumulatives = new int56[](secondsAgo.length);
        secondsPerLiquidityCumulativeX128s = new uint160[](secondsAgo.length);
    }

    /// @notice The pool tick spacing
    /// @dev Ticks can only be used at multiples of this value, minimum of 1 and always positive
    /// e.g.: a tickSpacing of 3 means ticks can be initialized every 3rd tick, i.e., ..., -6, -3, 0, 3, 6, ...
    /// This value is an int24 to avoid casting even though it is always positive.
    /// @return The tick spacing
    function tickSpacing() external view override returns (int24) {
        return 2;
    }

    /// @notice The 0th storage slot in the pool stores many values, and is exposed as a single method to save gas
    /// when accessed externally.
    /// @return sqrtPriceX96 The current price of the pool as a sqrt(token1/token0) Q64.96 value
    /// tick The current tick of the pool, i.e. according to the last tick transition that was run.
    /// This value may not always be equal to SqrtTickMath.getTickAtSqrtRatio(sqrtPriceX96) if the price is on a tick
    /// boundary.
    /// observationIndex The index of the last oracle observation that was written,
    /// observationCardinality The current maximum number of observations stored in the pool,
    /// observationCardinalityNext The next maximum number of observations, to be updated when the observation.
    /// feeProtocol The protocol fee for both tokens of the pool.
    /// Encoded as two 4 bit values, where the protocol fee of token1 is shifted 4 bits and the protocol fee of token0
    /// is the lower 4 bits. Used as the denominator of a fraction of the swap fee, e.g. 4 means 1/4th of the swap fee.
    /// unlocked Whether the pool is currently locked to reentrancy
    function slot0()
        external
        view
        override
        returns (
            uint160 sqrtPriceX96,
            int24 tick,
            uint16 observationIndex,
            uint16 observationCardinality,
            uint16 observationCardinalityNext,
            uint8 feeProtocol,
            bool unlocked
        )
    {
        return (uint160(ratio), 13863, 0, 0, 0, 0, true);
    }

    /// @notice Returns the information about a position by the position's key
    /// @param key The position's key is a hash of a preimage composed by the owner, tickLower and tickUpper
    /// @return _liquidity The amount of liquidity in the position,
    /// Returns feeGrowthInside0LastX128 fee growth of token0 inside the tick range as of the last mint/burn/poke,
    /// Returns feeGrowthInside1LastX128 fee growth of token1 inside the tick range as of the last mint/burn/poke,
    /// Returns tokensOwed0 the computed amount of token0 owed to the position as of the last mint/burn/poke,
    /// Returns tokensOwed1 the computed amount of token1 owed to the position as of the last mint/burn/poke
    function positions(bytes32 key)
        external
        view
        override
        returns (
            uint128 _liquidity,
            uint256 feeGrowthInside0LastX128,
            uint256 feeGrowthInside1LastX128,
            uint128 tokensOwed0,
            uint128 tokensOwed1
        )
    {
        // return (
        //     uint128(liquidity),
        //     uint256(0),
        //     uint256(0),
        //     uint128(owed0),
        //     uint128(owed1)
        // );
        require(liquidity < 2**128);
        _liquidity = uint128(liquidity);
        feeGrowthInside0LastX128 = 0;
        feeGrowthInside1LastX128 = 0;
        tokensOwed0 = owed0;
        tokensOwed1 = owed1;
    }
}
