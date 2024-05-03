// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IMakerManager {
    function cdpCan(address, uint, address) external view returns (uint);
    function ilks(uint) external view returns (bytes32);
    function owns(uint) external view returns (address);
    function urns(uint) external view returns (address);
    function vat() external view returns (address);
    function open(bytes32, address) external returns (uint);
    function give(uint, address) external;
    function cdpAllow(uint, address, uint) external;
    function urnAllow(address, uint) external;
    function frob(uint, int, int) external;
    function flux(uint, address, uint) external;
    function move(uint, address, uint) external;
    function exit(address, uint, address, uint) external;
    function quit(uint, address) external;
    function enter(address, uint) external;
    function shift(uint, uint) external;

    function count(address) external view returns (uint256);
    function first(address) external view returns (uint256);
    function last(address) external view returns (uint256);
}

interface IMakerVat {
    function can(address, address) external view returns (uint);
    function ilks(bytes32) external view returns (uint, uint, uint, uint, uint);
    function dai(address) external view returns (uint);
    function urns(bytes32, address) external view returns (uint, uint);
    function frob(bytes32, address, address, address, int, int) external;
    function hope(address) external;
    function move(address, address, uint) external;
}

interface IMakerGemJoin {
    function dec() external view returns (uint);
    function gem() external view returns (address);
    function join(address, uint) external payable;
    function exit(address, uint) external;
}

interface IMakerChainLog {
    function getAddress(bytes32) external view returns (address);
}
