// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface ILiquidityGauge {
    function lp_token() external view returns (address);
    function balanceOf(address arg0) external view returns (uint256);

    function set_approve_deposit(address addr, bool can_deposit) external;
    function deposit(uint256 _value, address addr) external;
    function withdraw(uint256 _value) external;
    function transfer(address _to, uint256 _value) external returns (bool);
    function claimable_tokens(address addr) external view returns (uint256);
}
