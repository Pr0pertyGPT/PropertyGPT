// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface KeeperRegistrarInterface {
  function register(
    string memory name,
    bytes calldata encryptedEmail,
    address upkeepContract,
    uint32 gasLimit,
    address adminAddress,
    bytes calldata checkData,
    uint96 amount,
    uint8 source,
    address sender
  ) external;
}
