// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";

contract ERC1155Mock is ERC1155 {
    uint256 public constant tokenId = 0;

    constructor() ERC1155("https://mock.example/api/item/{id}.json") {
        _mint(msg.sender, tokenId, 10 ** 18, "");
    }
}
