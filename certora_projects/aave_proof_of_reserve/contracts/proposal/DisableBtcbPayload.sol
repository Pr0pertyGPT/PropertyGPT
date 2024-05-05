// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {DataTypes, IPoolAddressesProvider, IPool, IPoolConfigurator} from 'aave-address-book/AaveV3.sol';
import {AaveV2Avalanche, AaveV3Avalanche} from 'aave-address-book/AaveAddressBook.sol';
import {IProofOfReserveExecutor} from '../interfaces/IProofOfReserveExecutor.sol';
import {ReserveConfiguration} from '../helpers/ReserveConfiguration.sol';

/**
 * @title DisableBtcbPayload
 * @author BGD Labs
 * @dev Payload to unfreeze btc.b asset and disable it on both executors.
 */

contract DisableBtcbPayload {
  IProofOfReserveExecutor public constant EXECUTOR_V2 =
    IProofOfReserveExecutor(0x7fc3FCb14eF04A48Bb0c12f0c39CD74C249c37d8);
  IProofOfReserveExecutor public constant EXECUTOR_V3 =
    IProofOfReserveExecutor(0xab22988D93d5F942fC6B6c6Ea285744809D1d9Cc);

  address public constant BTCB = 0x152b9d0FdC40C096757F570A51E494bd4b943E50;
  uint256 public constant LTV = 7000;

  function execute() external {
    address[] memory assetsToDisable = new address[](1);
    assetsToDisable[0] = BTCB;

    // disable BTCB on the V2 executor
    EXECUTOR_V2.disableAssets(assetsToDisable);

    // disable BTCB on the V3 executor
    EXECUTOR_V3.disableAssets(assetsToDisable);

    // get asset configuration
    DataTypes.ReserveConfigurationMap memory configuration = AaveV3Avalanche
      .POOL
      .getConfiguration(BTCB);
    (
      ,
      uint256 liquidationThreshold,
      uint256 liquidationBonus,

    ) = ReserveConfiguration.getReserveParams(configuration);

    // set LTV back to normal
    AaveV3Avalanche.POOL_CONFIGURATOR.configureReserveAsCollateral(
      BTCB,
      LTV,
      liquidationThreshold,
      liquidationBonus
    );

    // unfreeze reserve
    AaveV3Avalanche.POOL_CONFIGURATOR.setReserveFreeze(BTCB, false);
  }
}
