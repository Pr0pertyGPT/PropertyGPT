// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IProofOfReserveExecutor {
  /**
   * @dev emitted when new asset is enabled or disabled
   * @param asset the address of the asset
   * @param enabled whether it was enabled or disabled
   */
  event AssetStateChanged(address indexed asset, bool enabled);

  /**
   * @dev emitted when asset is not backed
   * @param asset asset that is not backed
   */
  event AssetIsNotBacked(address indexed asset);

  /**
   * @dev emitted when the emergency action is activated
   */
  event EmergencyActionExecuted();

  /**
   * @dev gets the list of the assets to check
   * @return returns all the assets that were enabled
   */
  function getAssets() external view returns (address[] memory);

  /**
   * @dev enable checking of proof of reserve for the passed list of assets
   * @param assets the addresses of the assets
   */
  function enableAssets(address[] memory assets) external;

  /**
   * @dev delete the assets and the proof of reserve feeds from the registry.
   * @param assets addresses of the assets
   */
  function disableAssets(address[] memory assets) external;

  /**
   * @dev returns if all the assets in the registry are backed.
   * @return bool returns true if all reserves are backed, otherwise false
   */
  function areAllReservesBacked() external view returns (bool);

  /**
   * @dev returns if emergency action parameters are not already adjusted.
   * This is not checked in executeEmergencyAction(), but is used
   * to prevent infinite execution of performUpkeep() inside the Keeper contract.
   * @return bool if it makes sense to execute the emergency action
   */
  function isEmergencyActionPossible() external view returns (bool);

  /**
   * @dev executes pool-specific action when at least
   * one of the assets in the registry is not backed.
   * v2: disable all borrowing and freeze the exploited assets
   * v3: set ltv to 0 for the broken assets and freeze them
   */
  function executeEmergencyAction() external;
}
