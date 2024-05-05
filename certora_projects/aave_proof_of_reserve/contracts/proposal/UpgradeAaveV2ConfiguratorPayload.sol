// SPDX-License-Identifier: MIT
pragma experimental ABIEncoderV2;
pragma solidity >=0.6.0;

import {LendingPoolConfigurator} from '@aave/core-v2/contracts/protocol/lendingpool/LendingPoolConfigurator.sol';
import {ILendingPoolAddressesProvider} from '@aave/core-v2/contracts/interfaces/ILendingPoolAddressesProvider.sol';

/**
 * @title UpgradeAaveV2ConfiguratorPayload
 * @author BGD Labs
 * @dev Proposal to deploy Proof Of Reserve and enable it as proofOfReserve admin for V2 and risk admin for V3.
 * - V2: upgrade implementation of LendingPoolConfigurator to enable new PROOF_OF_RESERVE_ADMIN role usage
 * - V2: assign PROOF_OF_RESERVE_ADMIN role to ProofOfReserveExecutorV2 in AddressProvider
 * Governance Forum Post: https://governance.aave.com/t/bgd-aave-chainlink-proof-of-reserve-phase-1-release-candidate/10972
 * Snapshot: https://snapshot.org/#/aave.eth/proposal/0x546ead37609b3f23c11559fe90e798b725af755f402bdd77e37583b4186d1f29
 */

contract UpgradeAaveV2ConfiguratorPayload {
  address public immutable EXECUTOR_V2;
  bytes32 public constant PROOF_OF_RESERVE_ADMIN = 'PROOF_OF_RESERVE_ADMIN';

  ILendingPoolAddressesProvider public immutable POOL_ADDRESSES_PROVIDER;

  constructor(address executorV2) public {
    EXECUTOR_V2 = executorV2;
    POOL_ADDRESSES_PROVIDER = ILendingPoolAddressesProvider(
      0xb6A86025F0FE1862B372cb0ca18CE3EDe02A318f // Avalanche V2 Addresses Provider
    );
  }

  function execute() external {
    // deploy & init lending pool configurator
    LendingPoolConfigurator poolConfigurator = new LendingPoolConfigurator();
    poolConfigurator.initialize(POOL_ADDRESSES_PROVIDER);

    // set the new implementation for Pool Configurator to enable PROOF_OF_RESERVE_ADMIN
    POOL_ADDRESSES_PROVIDER.setLendingPoolConfiguratorImpl(
      address(poolConfigurator)
    );

    // set ProofOfReserveExecutorV2 as PROOF_OF_RESERVE_ADMIN
    POOL_ADDRESSES_PROVIDER.setAddress(
      PROOF_OF_RESERVE_ADMIN,
      address(EXECUTOR_V2)
    );
  }
}
