// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {IERC20} from 'solidity-utils/contracts/oz-common/interfaces/IERC20.sol';
import {IERC20Metadata} from 'solidity-utils/contracts/oz-common/interfaces/IERC20Metadata.sol';

import {IBridgeWrapper} from '../interfaces/IBridgeWrapper.sol';

/**
 * @author BGD Labs
 * @dev Contract to wrap total supply of bridged tokens on Avalanche as there can possibly be
 * two bridges for one asset
 */
contract AvaxBridgeWrapper is IBridgeWrapper {
  // contract for the actual bridge
  IERC20Metadata private immutable _currentBridge;
  // contract for the deprecated bridge
  IERC20 private immutable _deprecatedBridge;

  /**
   * @notice Constructor.
   * @param currentBridgeAddress The address of the actual bridge for token
   * @param deprecatedBridgeAddress The address of the deprecated bridge for token
   */
  constructor(address currentBridgeAddress, address deprecatedBridgeAddress) {
    _currentBridge = IERC20Metadata(currentBridgeAddress);
    _deprecatedBridge = IERC20(deprecatedBridgeAddress);
  }

  /// @inheritdoc IBridgeWrapper
  function totalSupply() external view returns (uint256) {
    return _currentBridge.totalSupply() + _deprecatedBridge.totalSupply();
  }

  /// @inheritdoc IBridgeWrapper
  function name() external view returns (string memory) {
    return _currentBridge.name();
  }

  /// @inheritdoc IBridgeWrapper
  function symbol() external view returns (string memory) {
    return _currentBridge.symbol();
  }

  /// @inheritdoc IBridgeWrapper
  function decimals() external view returns (uint8) {
    return _currentBridge.decimals();
  }

  /// @inheritdoc IBridgeWrapper
  function getCurrentBridge() external view returns (address) {
    return address(_currentBridge);
  }

  /// @inheritdoc IBridgeWrapper
  function getDeprecatedBridge() external view returns (address) {
    return address(_deprecatedBridge);
  }
}
