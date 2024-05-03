// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IComptroller {
    function enterMarkets  (address[] calldata cTokens) external returns (uint[] memory);
    function exitMarket(address cToken) external returns (uint);
    function checkMembership(address account, address cToken) external view returns (bool);
    function claimComp(address holder) external;
    function getCompAddress() external view returns(address);
}
