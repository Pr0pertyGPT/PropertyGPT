// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {LinkTokenInterface} from 'chainlink-brownie-contracts/interfaces/LinkTokenInterface.sol';
import {KeeperRegistryInterface, Config, State} from 'chainlink-brownie-contracts/interfaces/KeeperRegistryInterface.sol';
import {KeeperRegistrarInterface} from './KeeperRegistrarInterface.sol';
import {ILendingPoolAddressesProvider} from 'aave-address-book/AaveV2.sol';
import {IACLManager} from 'aave-address-book/AaveV3.sol';
import {IProofOfReserveAggregator} from '../interfaces/IProofOfReserveAggregator.sol';
import {IProofOfReserveExecutor} from '../interfaces/IProofOfReserveExecutor.sol';
import {ICollectorController} from '../dependencies/ICollectorController.sol';
import {AvaxBridgeWrapper} from '../contracts/AvaxBridgeWrapper.sol';
import {IERC20} from 'solidity-utils/contracts/oz-common/interfaces/IERC20.sol';
import {AaveV2Avalanche, AaveV3Avalanche} from 'aave-address-book/AaveAddressBook.sol';

struct BridgeWrappers {
  address aave;
  address weth;
  address dai;
  address link;
  address wbtc;
}

/**
 * @title ProposalPayloadProofOfReserve
 * @author BGD Labs
 * @dev Proposal to deploy Proof Of Reserve and enable it as proofOfReserve admin for V2 and risk admin for V3.
 * - Add pairs of token and its proof of reserves to Proof Of Reserves Aggregator
 * - V2: upgrade implementation of LendingPoolConfigurator to enable new PROOF_OF_RESERVE_ADMIN role usage
 * - V2: assign PROOF_OF_RESERVE_ADMIN role to ProofOfReserveExecutorV2 in AddressProvider
 * - V2: enable tokens for checking against their proof of reserve feed
 * - V3: assign Risk admin role to ProofOfReserveExecutorV3
 * - Transfer aAvaLINK tokens from AAVE treasury to the current address, then withdraw them to get LINK.e
 * - Register V2 and V3 upkeeps for the Chainlink Keeper
 * Governance Forum Post: https://governance.aave.com/t/bgd-aave-chainlink-proof-of-reserve-phase-1-release-candidate/10972
 * Snapshot: https://snapshot.org/#/aave.eth/proposal/0x546ead37609b3f23c11559fe90e798b725af755f402bdd77e37583b4186d1f29
 */

contract ProposalPayloadProofOfReserve {
  bytes32 public constant PROOF_OF_RESERVE_ADMIN = 'PROOF_OF_RESERVE_ADMIN';

  IProofOfReserveAggregator public immutable AGGREGATOR;
  IProofOfReserveExecutor public immutable EXECUTOR_V2;
  IProofOfReserveExecutor public immutable EXECUTOR_V3;
  ICollectorController public constant COLLECTOR_CONTROLLER =
    ICollectorController(AaveV3Avalanche.COLLECTOR_CONTROLLER);

  address public immutable PROOF_OF_RESERVE_KEEPER_ADDRESS;

  address public constant KEEPER_REGISTRAR_ADDRESS =
    address(0xDb8e8e2ccb5C033938736aa89Fe4fa1eDfD15a1d);

  IERC20 public constant AAVA_LINK_TOKEN =
    IERC20(0x191c10Aa4AF7C30e871E70C95dB0E4eb77237530);

  address public constant LINK_TOKEN_ADDRESS =
    address(0x5947BB275c521040051D82396192181b413227A3);

  KeeperRegistryInterface public constant KEEPER_REGISTRY =
    KeeperRegistryInterface(0x02777053d6764996e594c3E88AF1D58D5363a2e6);

  LinkTokenInterface public constant LINK_TOKEN =
    LinkTokenInterface(LINK_TOKEN_ADDRESS);

  address public immutable AAVE_BRIDGE_WRAPPER;
  address public immutable WETH_BRIDGE_WRAPPER;
  address public immutable DAI_BRIDGE_WRAPPER;
  address public immutable LINK_BRIDGE_WRAPPER;
  address public immutable WBTC_BRIDGE_WRAPPER;

  /**
   * @dev emitted when the new upkeep is registered in Chainlink
   * @param name name of the upkeep
   * @param upkeepId id of the upkeep in chainlink
   */
  event ChainlinkUpkeepRegistered(
    string indexed name,
    uint256 indexed upkeepId
  );

  /**
   * @dev constructor of the proposal
   * @param aggregator PoR aggregator
   * @param executorV2 PoR executor V2
   * @param executorV3 PoR executor V3
   * @param keeperAddress the address of the chainlink keeper
   * @param bridgeWrappers struct containing addresses of the bridge wrappers
   */
  constructor(
    IProofOfReserveAggregator aggregator,
    IProofOfReserveExecutor executorV2,
    IProofOfReserveExecutor executorV3,
    address keeperAddress,
    BridgeWrappers memory bridgeWrappers
  ) {
    AGGREGATOR = aggregator;
    EXECUTOR_V2 = executorV2;
    EXECUTOR_V3 = executorV3;

    PROOF_OF_RESERVE_KEEPER_ADDRESS = keeperAddress;

    AAVE_BRIDGE_WRAPPER = bridgeWrappers.aave;
    WETH_BRIDGE_WRAPPER = bridgeWrappers.weth;
    DAI_BRIDGE_WRAPPER = bridgeWrappers.dai;
    LINK_BRIDGE_WRAPPER = bridgeWrappers.link;
    WBTC_BRIDGE_WRAPPER = bridgeWrappers.wbtc;
  }

  /**
   * @dev helper method that returns the listed of bridged assets to be protected
   * @return the list of assets
   * @return the list of PoR feeds, source: https://data.chain.link/avalanche/mainnet/reserves
   * @return the list of bridge wrappers, source:
   */
  function _initProofOfReservesDetails()
    internal
    view
    returns (
      address[] memory,
      address[] memory,
      address[] memory
    )
  {
    address[] memory assets = new address[](6);
    address[] memory proofOfReserveFeeds = new address[](6);
    address[] memory bridgeWrappers = new address[](6);

    // AAVE.e
    assets[0] = 0x63a72806098Bd3D9520cC43356dD78afe5D386D9;
    proofOfReserveFeeds[0] = 0x14C4c668E34c09E1FBA823aD5DB47F60aeBDD4F7;
    bridgeWrappers[0] = AAVE_BRIDGE_WRAPPER;

    // WETH.e
    assets[1] = 0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB;
    proofOfReserveFeeds[1] = 0xDDaf9290D057BfA12d7576e6dADC109421F31948;
    bridgeWrappers[1] = WETH_BRIDGE_WRAPPER;

    // DAI.e
    assets[2] = 0xd586E7F844cEa2F87f50152665BCbc2C279D8d70;
    proofOfReserveFeeds[2] = 0x976D7fAc81A49FA71EF20694a3C56B9eFB93c30B;
    bridgeWrappers[2] = DAI_BRIDGE_WRAPPER;

    // LINK.e
    assets[3] = LINK_TOKEN_ADDRESS;
    proofOfReserveFeeds[3] = 0x943cEF1B112Ca9FD7EDaDC9A46477d3812a382b6;
    bridgeWrappers[3] = LINK_BRIDGE_WRAPPER;

    // WBTC.e
    assets[4] = 0x50b7545627a5162F82A992c33b87aDc75187B218;
    proofOfReserveFeeds[4] = 0xebEfEAA58636DF9B20a4fAd78Fad8759e6A20e87;
    bridgeWrappers[4] = WBTC_BRIDGE_WRAPPER;

    // BTC.b
    assets[5] = 0x152b9d0FdC40C096757F570A51E494bd4b943E50;
    proofOfReserveFeeds[5] = 0x99311B4bf6D8E3D3B4b9fbdD09a1B0F4Ad8e06E9;
    bridgeWrappers[5] = address(0);

    return (assets, proofOfReserveFeeds, bridgeWrappers);
  }

  function execute() external {
    (
      address[] memory assets,
      address[] memory proofOfReserveFeeds,
      address[] memory bridgeWrappers
    ) = _initProofOfReservesDetails();

    for (uint256 i = 0; i < assets.length; ++i) {
      // enable proof of reserve feeds for assets in the aggregator
      if (bridgeWrappers[i] != address(0)) {
        AGGREGATOR.enableProofOfReserveFeedWithBridgeWrapper(
          assets[i], // token address
          proofOfReserveFeeds[i], // PoR feed address
          bridgeWrappers[i] // bridge wrapper address
        );
      } else {
        AGGREGATOR.enableProofOfReserveFeed(
          assets[i], // token address
          proofOfReserveFeeds[i] // PoR feed address
        );
      }
    }

    // V2
    // enable checking of proof of reserve for the assets
    EXECUTOR_V2.enableAssets(assets);

    // V3
    // assign RiskAdmin role to ProofOfReserveExecutorV3
    AaveV3Avalanche.ACL_MANAGER.addRiskAdmin(address(EXECUTOR_V3));

    // enable checking of proof of reserve for the assets
    EXECUTOR_V3.enableAssets(assets);

    // transfer aAvaLink token from the treasury to the current address
    COLLECTOR_CONTROLLER.transfer(
      AAVA_LINK_TOKEN,
      address(this),
      10100000000000000000
    );

    // withdraw aAvaLINK from the aave pool and receive LINK.e
    AaveV3Avalanche.POOL.withdraw(
      LINK_TOKEN_ADDRESS,
      type(uint256).max,
      address(this)
    );

    // create chainlink upkeep for v2
    registerUpkeep(
      'AaveProofOfReserveKeeperV2',
      PROOF_OF_RESERVE_KEEPER_ADDRESS,
      2500000,
      address(this),
      abi.encode(address(EXECUTOR_V2)),
      5000000000000000000
    );

    // create chainlink upkeep for v3
    registerUpkeep(
      'AaveProofOfReserveKeeperV3',
      PROOF_OF_RESERVE_KEEPER_ADDRESS,
      2500000,
      address(this),
      abi.encode(address(EXECUTOR_V3)),
      5000000000000000000
    );
  }

  /**
   * @dev register keeper contract in chainlink
   * @param name name of the upkeep
   * @param upkeepContract the address of the keeper contract
   * @param gasLimit gas limit for the emergency action execution
   * @param adminAddress the address of the admin
   * @param checkData params for the check method
   * @param amount amount of LINK for the upkeep
   */
  function registerUpkeep(
    string memory name,
    address upkeepContract,
    uint32 gasLimit,
    address adminAddress,
    bytes memory checkData,
    uint96 amount
  ) internal {
    (
      State memory state,
      Config memory _c,
      address[] memory _k
    ) = KEEPER_REGISTRY.getState();
    uint256 oldNonce = state.nonce;
    bytes memory payload = abi.encode(
      name,
      0x0,
      upkeepContract,
      gasLimit,
      adminAddress,
      checkData,
      amount,
      0,
      address(this)
    );

    bytes4 registerSig = KeeperRegistrarInterface.register.selector;

    LINK_TOKEN.transferAndCall(
      KEEPER_REGISTRAR_ADDRESS,
      amount,
      bytes.concat(registerSig, payload)
    );

    (state, _c, _k) = KEEPER_REGISTRY.getState();

    if (state.nonce == oldNonce + 1) {
      uint256 upkeepID = uint256(
        keccak256(
          abi.encodePacked(
            blockhash(block.number - 1),
            address(KEEPER_REGISTRY),
            uint32(oldNonce)
          )
        )
      );

      emit ChainlinkUpkeepRegistered(name, upkeepID);
    } else {
      revert('auto-approve disabled');
    }
  }
}
