// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IBridgeWrapper {
  /**
   * @dev Returns the sum amount of tokens on deprecate and actual bridges.
   */
  function totalSupply() external view returns (uint256);

  /**
   * @dev Returns the name of the token.
   */
  function name() external view returns (string memory);

  /**
   * @dev Returns the symbol of the token.
   */
  function symbol() external view returns (string memory);

  /**
   * @dev Returns the decimals places of the token.
   */
  function decimals() external view returns (uint8);

  /**
   * @dev Returns the address of the current bridge.
   */
  function getCurrentBridge() external view returns (address);

  /**
   * @dev Returns the address of the deprecated bridge.
   */
  function getDeprecatedBridge() external view returns (address);
}
