// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.16;

import {AaveMisc} from 'aave-address-book/AaveMisc.sol';
import {AaveGovernanceV2} from 'aave-address-book/AaveGovernanceV2.sol';
import {AaveV2EthereumAssets} from 'aave-address-book/AaveV2Ethereum.sol';
import {ProxyAdmin} from 'solidity-utils/contracts/transparent-proxy/ProxyAdmin.sol';
import {TransparentUpgradeableProxy} from 'solidity-utils/contracts/transparent-proxy/TransparentUpgradeableProxy.sol';
import {StakedAaveV3} from './StakedAaveV3.sol';
import {StakedTokenV3} from './StakedTokenV3.sol';
import {IERC20} from '../interfaces/IERC20.sol';
import {IInitializableAdminUpgradeabilityProxy} from '../interfaces/IInitializableAdminUpgradeabilityProxy.sol';

library GenericProposal {
  address public constant SLASHING_ADMIN = AaveGovernanceV2.SHORT_EXECUTOR;

  address public constant COOLDOWN_ADMIN = AaveGovernanceV2.SHORT_EXECUTOR;

  address public constant CLAIM_HELPER = AaveGovernanceV2.SHORT_EXECUTOR;

  address public constant REWARDS_VAULT = AaveMisc.ECOSYSTEM_RESERVE;

  address public constant EMISSION_MANAGER = AaveGovernanceV2.SHORT_EXECUTOR;

  uint256 public constant MAX_SLASHING = 3000; // 30%

  uint256 public constant COOLDOWN_SECONDS = 1728000; // 20 days

  uint256 public constant UNSTAKE_WINDOW = 172800; // 2 days

  uint128 public constant DISTRIBUTION_DURATION = 3155692600; // 100 years
}

/**
 * @title ProposalPayloadStkAave
 * @notice Proposal for upgrading the StkAave implementation
 * @author BGD Labs
 */
contract ProposalPayloadStkAave {
  address public constant STK_AAVE = 0x4da27a545c0c5B758a6BA100e3a049001de870f5;

  function execute() external {
    // 1. move ownership of current token to new proxy
    IInitializableAdminUpgradeabilityProxy(STK_AAVE).changeAdmin(
      address(AaveMisc.PROXY_ADMIN_ETHEREUM_LONG)
    );
    // 2. deploy newimplementation
    StakedAaveV3 newImpl = new StakedAaveV3(
      IERC20(AaveV2EthereumAssets.AAVE_UNDERLYING),
      IERC20(AaveV2EthereumAssets.AAVE_UNDERLYING),
      GenericProposal.UNSTAKE_WINDOW,
      GenericProposal.REWARDS_VAULT,
      GenericProposal.EMISSION_MANAGER,
      GenericProposal.DISTRIBUTION_DURATION
    );
    // 3. upgrade & initialize on proxy
    ProxyAdmin(AaveMisc.PROXY_ADMIN_ETHEREUM_LONG).upgradeAndCall(
      TransparentUpgradeableProxy(payable(STK_AAVE)),
      address(newImpl),
      abi.encodeWithSignature(
        'initialize(address,address,address,uint256,uint256)',
        GenericProposal.SLASHING_ADMIN,
        GenericProposal.COOLDOWN_ADMIN,
        GenericProposal.CLAIM_HELPER,
        GenericProposal.MAX_SLASHING,
        GenericProposal.COOLDOWN_SECONDS
      )
    );
  }
}

/**
 * @title ProposalPayloadStkAbpt
 * @notice Proposal for upgrading the StkAbpt implementation
 * @author BGD Labs
 */
contract ProposalPayloadStkAbpt {
  address public constant STK_ABPT = 0xa1116930326D21fB917d5A27F1E9943A9595fb47;
  address public constant ABPT = 0x41A08648C3766F9F9d85598fF102a08f4ef84F84;

  function execute() external {
    // 1. move ownership of current token to new proxy
    IInitializableAdminUpgradeabilityProxy(STK_ABPT).changeAdmin(
      AaveMisc.PROXY_ADMIN_ETHEREUM
    );
    // 2. deploy newimplementation
    StakedTokenV3 newImpl = new StakedTokenV3(
      IERC20(ABPT),
      IERC20(AaveV2EthereumAssets.AAVE_UNDERLYING),
      GenericProposal.UNSTAKE_WINDOW,
      GenericProposal.REWARDS_VAULT,
      GenericProposal.EMISSION_MANAGER,
      GenericProposal.DISTRIBUTION_DURATION
    );
    // 3. upgrade & initialize on proxy
    ProxyAdmin(AaveMisc.PROXY_ADMIN_ETHEREUM).upgradeAndCall(
      TransparentUpgradeableProxy(payable(STK_ABPT)),
      address(newImpl),
      abi.encodeWithSignature(
        'initialize(address,address,address,uint256,uint256)',
        GenericProposal.SLASHING_ADMIN,
        GenericProposal.COOLDOWN_ADMIN,
        GenericProposal.CLAIM_HELPER,
        GenericProposal.MAX_SLASHING,
        GenericProposal.COOLDOWN_SECONDS
      )
    );
  }
}
