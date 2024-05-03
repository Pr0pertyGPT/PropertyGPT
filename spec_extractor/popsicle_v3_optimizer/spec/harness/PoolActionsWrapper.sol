pragma solidity 0.7.6;
pragma abicoder v2;

import {IUniswapV3Pool} from '../../contracts/popsicle-v3-optimizer/interfaces/IUniswapV3Pool.sol';
import {PoolVariables} from '../../contracts/popsicle-v3-optimizer/libraries/PoolVariables.sol';
import {SafeCast} from '../../contracts/popsicle-v3-optimizer/libraries/SafeCast.sol';
import {PoolActions} from '../../contracts/popsicle-v3-optimizer/libraries/PoolActions.sol';

contract PoolActionsWrapper{
    using PoolActions for *;
    
    IUniswapV3Pool public pool;
    uint256 totalSupply;
    // Accrued protocol fees in terms of token0
    // uint256 public protocolFees0;
    // Accrued protocol fees in terms of token1
    // uint256 public protocolFees1;
    uint128 protocolLiquidity;
    

    function callBurnLiquidityShare(
        int24 tickLower,
        int24 tickUpper,       
        uint256 share,
        address to   
    ) external returns (uint256 amount0, uint256 amount1) {
        // uint128 protocolLiquidity = pool.liquidityForAmounts(protocolFees0, protocolFees1, tickLower, tickUpper);
        (amount0 , amount1) = PoolActions.burnLiquidityShare(pool, tickLower, tickUpper, 
                                  totalSupply, share, to, protocolLiquidity);
    }

    /* iuniswap pool;?? */
    function callBurnExactLiquidity(
        int24 tickLower,
        int24 tickUpper,
        uint128 liquidity,
        address to
    ) external returns (uint256 amount0, uint256 amount1) {
        
        (amount0 , amount1) = PoolActions.burnExactLiquidity(pool, tickLower, tickUpper, liquidity, to);
    }

    function callBurnAllLiquidity(
        int24 tickLower,
        int24 tickUpper
    ) external {
        PoolActions.burnAllLiquidity(pool, tickLower, tickUpper);
    }
}
