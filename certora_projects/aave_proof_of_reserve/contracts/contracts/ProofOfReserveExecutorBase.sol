// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {Ownable} from 'solidity-utils/contracts/oz-common/Ownable.sol';
import {IERC20} from 'solidity-utils/contracts/oz-common/interfaces/IERC20.sol';
import {AggregatorV3Interface} from 'chainlink-brownie-contracts/interfaces/AggregatorV3Interface.sol';

import {IProofOfReserveExecutor} from '../interfaces/IProofOfReserveExecutor.sol';
import {IProofOfReserveAggregator} from '../interfaces/IProofOfReserveAggregator.sol';

/**
 * @author BGD Labs
 * @dev Aave pool-specific contract for Proof of Reserve validations:
 * - Stores list of token addresses that will be validated against their proof of reserve feed data
 * - Returns if all tokens of a list of assets are properly backed or not.
 */
abstract contract ProofOfReserveExecutorBase is
  IProofOfReserveExecutor,
  Ownable
{
  /// @dev proof of reserve aggregator contract that holds
  IProofOfReserveAggregator internal immutable _proofOfReserveAggregator;

  /// @dev the list of the tokens, which total supply we would check against data of the associated proof of reserve feed
  address[] internal _assets;

  /// @dev token address = > is it contained in the list
  mapping(address => bool) internal _assetsState;

  /**
   * @notice Constructor.
   * @param proofOfReserveAggregatorAddress The address of Proof of Reserve aggregator contract
   */
  constructor(address proofOfReserveAggregatorAddress) {
    _proofOfReserveAggregator = IProofOfReserveAggregator(
      proofOfReserveAggregatorAddress
    );
  }

  /// @inheritdoc IProofOfReserveExecutor
  function getAssets() external view returns (address[] memory) {
    return _assets;
  }

  /// @inheritdoc IProofOfReserveExecutor
  function enableAssets(address[] memory assets) external onlyOwner {
    for (uint256 i = 0; i < assets.length; ++i) {
      if (!_assetsState[assets[i]]) {
        _assets.push(assets[i]);
        _assetsState[assets[i]] = true;
        emit AssetStateChanged(assets[i], true);
      }
    }
  }

  /// @inheritdoc IProofOfReserveExecutor
  function disableAssets(address[] memory assets) external onlyOwner {
    for (uint256 i = 0; i < assets.length; ++i) {
      if (_assetsState[assets[i]]) {
        _deleteAssetFromArray(assets[i]);
        delete _assetsState[assets[i]];
        emit AssetStateChanged(assets[i], false);
      }
    }
  }

  /**
   * @dev delete asset from array.
   * @param asset the address to delete
   */
  function _deleteAssetFromArray(address asset) internal {
    uint256 assetsLength = _assets.length;

    for (uint256 i = 0; i < assetsLength; ++i) {
      if (_assets[i] == asset) {
        if (i != assetsLength - 1) {
          _assets[i] = _assets[assetsLength - 1];
        }

        _assets.pop();
        break;
      }
    }
  }

  /// @inheritdoc IProofOfReserveExecutor
  function areAllReservesBacked() external view returns (bool) {
    if (_assets.length == 0) {
      return true;
    }

    (bool areReservesBacked, ) = _proofOfReserveAggregator.areAllReservesBacked(
      _assets
    );

    return areReservesBacked;
  }

  /// @inheritdoc IProofOfReserveExecutor
  function isEmergencyActionPossible() external view virtual returns (bool);
}
