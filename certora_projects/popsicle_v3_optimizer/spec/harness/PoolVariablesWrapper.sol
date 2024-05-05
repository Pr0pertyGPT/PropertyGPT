pragma solidity >=0.5.0;

import {IUniswapV3Pool} from '../../contracts/popsicle-v3-optimizer/interfaces/IUniswapV3Pool.sol';
import {PoolVariables} from '../../contracts/popsicle-v3-optimizer/libraries/PoolVariables.sol';
// import '../../contracts/popsicle-v3-optimizer/libraries/LiquidityAmounts.sol';
// import '../../contracts/popsicle-v3-optimizer/interfaces/IUniswapV3Pool.sol';
/* import "../../contracts/popsicle-v3-optimizer/libraries/TickMath.sol";
import "../../contracts/popsicle-v3-optimizer/libraries/PositionKey.sol";
import "../../contracts/popsicle-v3-optimizer/libraries/LowGasSafeMath.sol";
import "../../contracts/popsicle-v3-optimizer/libraries/SqrtPriceMath.sol";
import {PoolVariables} from '../../contracts/popsicle-v3-optimizer/libraries/PoolVariables.sol'; */

contract PoolVariablesWrapper{
    using PoolVariables for *;
    IUniswapV3Pool pool;
    function callAmountsForLiquidity(
        uint128 liquidity,
        int24 _tickLower,
        int24 _tickUpper
    ) internal view returns (uint256, uint256){
        return PoolVariables.amountsForLiquidity(
                    pool, liquidity, _tickLower, _tickUpper);
    } 

    function callLiquidityForAmounts(
        uint256 amount0,
        uint256 amount1,
        int24 _tickLower,
        int24 _tickUpper
    ) external view returns (uint128){
        return PoolVariables.liquidityForAmounts(pool, amount0, amount1, _tickLower, _tickUpper);
    }

    // function callPositionAmounts(int24 _tickLower, int24 _tickUpper)
    //     external
    //     view
    //     returns (uint256 amount0, uint256 amount1){
    //         (amount0 , amount1) =  PoolVariables.positionAmounts(pool, _tickLower, _tickUpper);
    // }

    function callPositionLiquidity(int24 _tickLower, int24 _tickUpper)
        external
        view
        returns (uint128 liquidity){
        liquidity = PoolVariables.positionLiquidity(pool, _tickLower, _tickUpper);
    }

    function callCheckRange(int24 tickLower, int24 tickUpper) external pure {
        PoolVariables.checkRange(tickLower, tickUpper);
    }

    function callFloor(int24 tick, int24 tickSpacing) external pure returns (int24){
        return PoolVariables.floor(tick, tickSpacing);
    }

    function callGetPositionTicks(IUniswapV3Pool pool, uint256 amount0Desired, uint256 amount1Desired,
                              int24 baseThreshold, int24 tickSpacing) external view 
                                returns(int24 tickLower, int24 tickUpper) {
        (tickLower, tickUpper) = PoolVariables.getPositionTicks(pool, amount0Desired, amount1Desired, baseThreshold, tickSpacing);
    }

    function callAmountsForTicks(IUniswapV3Pool pool, uint256 amount0Desired, uint256 amount1Desired, 
        int24 _tickLower, int24 _tickUpper) external view returns(uint256 amount0, uint256 amount1){
        (amount0, amount1) = PoolVariables.amountsForTicks(pool, amount0Desired, amount1Desired, _tickLower, _tickUpper);
    }
    
    function callBaseTicks(int24 currentTick, int24 baseThreshold, int24 tickSpacing) external pure 
                returns(int24 tickLower, int24 tickUpper) {
        (tickLower, tickUpper) = PoolVariables.baseTicks(currentTick, baseThreshold, tickSpacing);
    }

    function callAmountsDirection(uint256 amount0Desired, uint256 amount1Desired, uint256 amount0, 
            uint256 amount1) external pure returns (bool zeroGreaterOne) {
        zeroGreaterOne = PoolVariables.amountsDirection(amount0Desired, amount1Desired, amount0, amount1);
    }

    function callcheckDeviation(int24 maxTwapDeviation, uint32 twapDuration) external view {
        PoolVariables.checkDeviation(pool, maxTwapDeviation, twapDuration);
    }

    function callGetTwap(uint32 twapDuration) internal view returns (int24){
        return PoolVariables.getTwap(pool, twapDuration);
    }
}