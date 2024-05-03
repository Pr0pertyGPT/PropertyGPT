// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;

import "../RuleBase.sol";
import "./IStarNFTV4.sol";

contract RStarNFTV4 is RuleBase {
    uint256 public immutable DISCOUNT;
    IStarNFTV4 public immutable starNFT;

    constructor(IStarNFTV4 nft_, uint256 discount_) {
        starNFT = nft_;
        DISCOUNT = discount_;
    }

    function verify(address usr_) public view returns (bool) {
        return starNFT.balanceOf(usr_) > 0;
    }

    function calDiscount(address usr_) external view returns (uint256) {
        return verify(usr_) ? DISCOUNT : BASE;
    }
}
