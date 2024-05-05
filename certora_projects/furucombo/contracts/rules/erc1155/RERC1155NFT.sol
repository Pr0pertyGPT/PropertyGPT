// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC1155/IERC1155.sol";
import "../RuleBase.sol";

contract RERC1155NFT is RuleBase {
    uint256 public immutable DISCOUNT;
    uint256 public immutable tokenId;
    IERC1155 public immutable nft;

    constructor(IERC1155 nft_, uint256 discount_, uint256 tokenId_) {
        nft = nft_;
        tokenId = tokenId_;
        DISCOUNT = discount_;
    }

    function verify(address usr_) public view returns (bool) {
        return nft.balanceOf(usr_, tokenId) > 0;
    }

    function calDiscount(address usr_) external view returns (uint256) {
        return verify(usr_) ? DISCOUNT : BASE;
    }
}
