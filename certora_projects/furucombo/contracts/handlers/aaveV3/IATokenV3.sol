// SPDX-License-Identifier: AGPL-3.0
pragma solidity ^0.8.0;

interface IATokenV3 {

    // IAToken
    function mint(address user, uint256 amount, uint256 index) external returns (bool);
    function burn(address from, address receiverOfUnderlying, uint256 amount, uint256 index) external;
    function mintToTreasury(uint256 amount, uint256 index) external;
    function transferOnLiquidation(address from, address to, uint256 value) external;
    function transferUnderlyingTo(address user, uint256 amount) external;
    function handleRepayment(address user, uint256 amount) external;
    function permit(address owner, address spender, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s) external;
    function UNDERLYING_ASSET_ADDRESS() external view returns (address);
    function RESERVE_TREASURY_ADDRESS() external view returns (address);
    function DOMAIN_SEPARATOR() external view returns (bytes32);
    function nonces(address owner) external view returns (uint256);
    function rescueTokens(address token, address to, uint256 amount) external;

    // IScaledBalanceToken
    function scaledBalanceOf(address user) external view returns (uint256);
    function getScaledUserBalanceAndSupply(address user) external view returns (uint256, uint256);
    function scaledTotalSupply() external view returns (uint256);

    // IERC20
    function totalSupply() external view returns (uint256 supply);
    function balanceOf(address _owner) external view returns (uint256 balance);
    function transfer(address _to, uint256 _value) external returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) external returns (bool success);
    function approve(address _spender, uint256 _value) external returns (bool success);
    function allowance(address _owner, address _spender) external view returns (uint256 remaining);
    function name() external view returns (string memory);
    function symbol() external view returns (string memory);
    function decimals() external view returns (uint8);
}