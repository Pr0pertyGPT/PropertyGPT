// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {Ownable} from 'solidity-utils/contracts/oz-common/Ownable.sol';
import {IERC20} from 'solidity-utils/contracts/oz-common/interfaces/IERC20.sol';
import {AggregatorV3Interface} from 'chainlink-brownie-contracts/interfaces/AggregatorV3Interface.sol';

import {IProofOfReserveAggregator} from '../interfaces/IProofOfReserveAggregator.sol';

/**
 * @author BGD Labs
 * @dev Aave aggregator contract for Proof of Reserve Feeds and validations based on them:
 * - Indexes proof of reserve feed by token address
 * - Returns if all tokens of a list of assets are properly backed with Proof of Reserve logic, or not.
 */
contract ProofOfReserveAggregator is IProofOfReserveAggregator, Ownable {
  /// @dev token address => proof or reserve feed
  mapping(address => address) internal _proofOfReserveList;

  /// @dev token address = > bridge wrapper
  mapping(address => address) internal _bridgeWrapperList;

  /// @inheritdoc IProofOfReserveAggregator
  function getProofOfReserveFeedForAsset(address asset)
    external
    view
    returns (address)
  {
    return _proofOfReserveList[asset];
  }

  /// @inheritdoc IProofOfReserveAggregator
  function getBridgeWrapperForAsset(address asset)
    external
    view
    returns (address)
  {
    return _bridgeWrapperList[asset];
  }

  /// @inheritdoc IProofOfReserveAggregator
  function enableProofOfReserveFeed(address asset, address proofOfReserveFeed)
    external
    onlyOwner
  {
    require(asset != address(0), 'INVALID_ASSET');
    require(proofOfReserveFeed != address(0), 'INVALID_PROOF_OF_RESERVE_FEED');
    require(_proofOfReserveList[asset] == address(0), 'FEED_ALREADY_ENABLED');

    _proofOfReserveList[asset] = proofOfReserveFeed;
    emit ProofOfReserveFeedStateChanged(
      asset,
      proofOfReserveFeed,
      address(0),
      true
    );
  }

  /// @inheritdoc IProofOfReserveAggregator
  function enableProofOfReserveFeedWithBridgeWrapper(
    address asset,
    address proofOfReserveFeed,
    address bridgeWrapper
  ) external onlyOwner {
    require(asset != address(0), 'INVALID_ASSET');
    require(proofOfReserveFeed != address(0), 'INVALID_PROOF_OF_RESERVE_FEED');
    require(bridgeWrapper != address(0), 'INVALID_BRIDGE_WRAPPER');
    require(_proofOfReserveList[asset] == address(0), 'FEED_ALREADY_ENABLED');

    _proofOfReserveList[asset] = proofOfReserveFeed;
    _bridgeWrapperList[asset] = bridgeWrapper;

    emit ProofOfReserveFeedStateChanged(
      asset,
      proofOfReserveFeed,
      bridgeWrapper,
      true
    );
  }

  /// @inheritdoc IProofOfReserveAggregator
  function disableProofOfReserveFeed(address asset) external onlyOwner {
    delete _proofOfReserveList[asset];
    delete _bridgeWrapperList[asset];
    emit ProofOfReserveFeedStateChanged(asset, address(0), address(0), false);
  }

  /// @inheritdoc IProofOfReserveAggregator
  function areAllReservesBacked(address[] calldata assets)
    external
    view
    returns (bool, bool[] memory)
  {
    bool[] memory unbackedAssetsFlags = new bool[](assets.length);
    bool areReservesBacked = true;

    unchecked {
      for (uint256 i = 0; i < assets.length; ++i) {
        address assetAddress = assets[i];
        address feedAddress = _proofOfReserveList[assetAddress];
        address bridgeAddress = _bridgeWrapperList[assetAddress];
        address totalSupplyAddress = bridgeAddress != address(0)
          ? bridgeAddress
          : assetAddress;

        if (feedAddress != address(0)) {
          (, int256 answer, , , ) = AggregatorV3Interface(feedAddress)
            .latestRoundData();

          if (
            answer < 0 ||
            IERC20(totalSupplyAddress).totalSupply() > uint256(answer)
          ) {
            unbackedAssetsFlags[i] = true;
            areReservesBacked = false;
          }
        }
      }
    }

    return (areReservesBacked, unbackedAssetsFlags);
  }
}
