// SPDX-License-Identifier: GPL-3.0-only
pragma solidity ^0.7.0;

import "interfaces/notional/AssetRateAdapter.sol";
import "interfaces/compound/CTokenInterface.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/math/SafeMath.sol";

// TODO: is this necessary?
contract cTokenAggregator is AssetRateAdapter {
    using SafeMath for uint256;

    address public override token;
    uint8 public override decimals = 18;
    uint256 public override version = 1;
    string public override description;
    uint256 public constant BLOCKS_PER_YEAR = 2102400;
    // Notional rate precision = 1e9
    // Compound rate precision = 1e18
    uint256 public constant SCALE_RATE = 1e9;

    constructor(address _cToken) {
        token = _cToken;
        description = ERC20(_cToken).symbol();
    }

    function underlying() external view override returns (address) {
        return CTokenInterface(token).underlying();
    }

    /** @notice Returns the current exchange rate for the cToken to the underlying */
    function getExchangeRateStateful() external override returns (int256) {
        uint256 exchangeRate = CTokenInterface(token).exchangeRateCurrent();
        require(exchangeRate <= uint256(type(int256).max), "cTokenAdapter: overflow");

        return int256(exchangeRate);
    }

    function getExchangeRateView() external view override returns (int256) {
        uint256 exchangeRate = CTokenInterface(token).exchangeRateStored();
        require(exchangeRate <= uint256(type(int256).max), "cTokenAdapter: overflow");

        return int256(exchangeRate);
    }

    function getAnnualizedSupplyRate() external view override returns (uint256) {
        uint256 supplyRatePerBlock = CTokenInterface(token).supplyRatePerBlock();

        // Supply rate per block * blocks per year * notional rate precision / supply rate precision
        return supplyRatePerBlock.mul(BLOCKS_PER_YEAR).div(SCALE_RATE);
    }
}
