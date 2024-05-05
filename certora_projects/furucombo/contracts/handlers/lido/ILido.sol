// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;


interface ILido {
    function submit(address _referral) external payable returns (uint256);
    function sharesOf(address _account) external view returns (uint256);
    function getPooledEthByShares(uint256 _sharesAmount) external view returns (uint256);

}
